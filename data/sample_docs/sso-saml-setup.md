# Setting Up SSO with SAML

Single sign-on (SSO) via SAML 2.0 is available on Growth and Enterprise plans. With SSO enabled, your team signs in to Flowstack through your identity provider (IdP) instead of managing separate passwords.

## Prerequisites

- You must be a workspace **Admin**.
- Your identity provider must support SAML 2.0 (Okta, Microsoft Entra ID / Azure AD, Google Workspace, and OneLogin are all supported).

## Configuration Steps

1. In Flowstack, go to **Settings → Security → Single Sign-On** and click **Enable SAML**.
2. Copy the **ACS URL** and **Entity ID** shown on screen.
3. In your IdP, create a new SAML application and paste in the ACS URL and Entity ID.
4. Download the IdP metadata XML (or copy the SSO URL and X.509 certificate) and upload it back into Flowstack.
5. Map attributes: `email` (required), `firstName`, and `lastName` (optional).
6. Click **Test login** — Flowstack will open your IdP in a new tab so you can verify the handshake works before enforcing it.
7. Optionally enable **Enforce SSO** to require all members to sign in via the IdP, disabling password login.

## Okta Example

In Okta: Applications → Create App Integration → SAML 2.0. Set the Single sign-on URL to the Flowstack ACS URL and the Audience URI to the Entity ID. Under Attribute Statements add `email → user.email`, `firstName → user.firstName`, `lastName → user.lastName`. Assign the app to your Flowstack users or groups, then download the metadata and finish setup in Flowstack.

## SCIM Provisioning

Enterprise plans support SCIM 2.0 for automatic provisioning and deprovisioning. When enabled, creating a user in your IdP automatically creates their Flowstack account, and deactivating them in the IdP suspends their Flowstack access within 15 minutes. Generate a SCIM bearer token from the SSO settings page to configure your IdP.

## Troubleshooting

If logins fail, check that the system clock on your IdP is accurate (SAML assertions are time-sensitive), that the certificate has not expired, and that the email attribute matches the user's Flowstack account email exactly.
