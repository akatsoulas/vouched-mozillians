from django.http import HttpRequest
from django.test import override_settings

from mock import Mock
from nose.tools import eq_, ok_

from mozillians.common.tests import TestCase
from mozillians.users.models import IdpProfile
from mozillians.users.tests import UserFactory


class MozilliansAuthBackendTests(TestCase):
    """Test Mozillian's Authentication Backend."""

    @override_settings(OIDC_OP_TOKEN_ENDPOINT="https://server.example.com/token")
    @override_settings(OIDC_OP_USER_ENDPOINT="https://server.example.com/user")
    @override_settings(OIDC_RP_CLIENT_ID="example_id")
    @override_settings(OIDC_RP_CLIENT_SECRET="client_secret")
    def setUp(self):
        """Setup class."""

        # Avoid circular dependencies
        from mozillians.common.authbackend import MozilliansAuthBackend

        self.backend = MozilliansAuthBackend()

    def test_add_a_new_email_identity(self):
        """Test to add a new email in an authenticated user."""
        user = UserFactory.create(email="foo@example.com")
        IdpProfile.objects.create(
            profile=user.userprofile,
            auth0_user_id="email|",
            email=user.email,
            primary=True,
        )
        claims = {"email": "bar@example.com", "user_id": "ad|ldap"}

        request_mock = Mock(spec=HttpRequest)
        request_mock.user = user
        self.backend.claims = claims
        self.backend.request = request_mock

        email_q = IdpProfile.objects.filter(
            profile=user.userprofile, email="bar@example.com"
        )
        ok_(not email_q.exists())
        returned_user = self.backend.check_authentication_method(user)
        email_q = IdpProfile.objects.filter(
            profile=user.userprofile, email="bar@example.com"
        )
        ok_(email_q.exists())
        eq_(returned_user, user)

    def test_identity_already_exists(self):
        """Test to add an email that already exists."""

        user = UserFactory.create(email="foo@example.com")
        IdpProfile.objects.create(
            profile=user.userprofile,
            auth0_user_id="email|",
            email=user.email,
            primary=True,
        )
        claims = {"email": "foo@example.com", "user_id": "email|"}

        request_mock = Mock(spec=HttpRequest)
        request_mock.user = user
        self.backend.claims = claims
        self.backend.request = request_mock
        self.backend.check_authentication_method(user)
        idp_q = IdpProfile.objects.filter(
            auth0_user_id="email|", email=user.email, profile=user.userprofile
        )
        eq_(idp_q.count(), 1)

    def test_identity_single_auth0_id_multiple_emails(self):
        """Test to add an email that already exists."""

        user = UserFactory.create(email="foo@example.com")
        IdpProfile.objects.create(
            profile=user.userprofile,
            auth0_user_id="github|12345",
            email="foo@bar.com",
            primary=True,
        )
        claims = {
            "email": "foo@example.com",
            "user_id": "github|12345",
            "nickname": "foo",
        }

        request_mock = Mock(spec=HttpRequest)
        request_mock.user = user
        self.backend.claims = claims
        self.backend.request = request_mock
        self.backend.check_authentication_method(user)

        eq_(
            IdpProfile.objects.filter(
                profile=user.userprofile,
                primary=True,
                username="foo",
                email="foo@example.com",
            ).count(),
            1,
        )
        eq_(
            IdpProfile.objects.filter(
                profile=user.userprofile, primary=False, email="foo@bar.com"
            ).count(),
            1,
        )

    def test_filter_users_with_email_belonging_to_non_primary_identity(self):
        """Test filter users with a non primary identity."""

        user = UserFactory.create(email="foo@example.com")
        IdpProfile.objects.create(
            profile=user.userprofile,
            auth0_user_id="email|1",
            email="bar@example.com",
            primary=True,
        )
        claims = {"email": "bar@example.com", "user_id": "email|1"}

        request_mock = Mock(spec=HttpRequest)
        request_mock.user = user
        self.backend.claims = claims
        self.backend.request = request_mock
        users = self.backend.filter_users_by_claims(claims)
        idp_q = IdpProfile.objects.filter(
            auth0_user_id="email|1", email="bar@example.com", profile=user.userprofile
        )
        eq_(idp_q.count(), 1)
        eq_(users[0], user)

    def test_filter_users_with_a_non_existing_identity(self):
        """Test filter users with a non primary identity."""

        user = UserFactory.create(email="foo@example.com")
        IdpProfile.objects.create(
            profile=user.userprofile,
            auth0_user_id="email|1",
            email="foo@example.com",
            primary=True,
        )
        claims = {"email": "bar@example.com", "user_id": "email|2"}

        request_mock = Mock(spec=HttpRequest)
        request_mock.user = user
        self.backend.claims = claims
        self.backend.request = request_mock
        users = self.backend.filter_users_by_claims(claims)
        idp_q = IdpProfile.objects.filter(
            auth0_user_id="email|1", email="foo@example.com", profile=user.userprofile
        )
        eq_(idp_q.count(), 1)
        eq_(list(users), [])

    @override_settings(CAN_VOUCH_THRESHOLD=1)
    def test_auto_vouching(self):
        claims = {
            "email": "foo@example.com",
            "user_id": "ad|foo@example.com",
            "https://sso.mozilla.com/claim/groups": ["hris_is_staff"],
        }
        user = UserFactory.create(vouched=False, email="foo@example.com")
        IdpProfile.objects.create(
            profile=user.userprofile,
            auth0_user_id="ad|foo@example.com",
            email="foo@example.com",
            primary=True,
        )
        request_mock = Mock(spec=HttpRequest)
        request_mock.user = user
        self.backend.claims = claims
        self.backend.request = request_mock
        returned_user = self.backend.check_authentication_method(user)
        ok_(returned_user.userprofile.is_vouched)
        eq_(returned_user.userprofile.vouches_received.all()[0].autovouch, True)

    def test_auto_vouching_missing_is_staff_attribute(self):
        claims = {
            "email": "foo@example.com",
            "user_id": "ad|bar@example.com",
            "https://sso.mozilla.com/claim/groups": ["hello world"],
        }
        user = UserFactory.create(vouched=False, email="bar@example.com")
        IdpProfile.objects.create(
            profile=user.userprofile,
            auth0_user_id="ad|bar@example.com",
            email="bar@example.com",
            primary=True,
        )
        request_mock = Mock(spec=HttpRequest)
        request_mock.user = user
        self.backend.claims = claims
        self.backend.request = request_mock
        returned_user = self.backend.check_authentication_method(user)
        ok_(not returned_user.userprofile.is_vouched)
