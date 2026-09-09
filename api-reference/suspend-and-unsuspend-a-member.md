---
title: Suspend or Unsuspend a Member Account
type: API guide
original_format: PDF (published help center article)
---

# Suspend or Unsuspend a Member Account

How to turn MURAL access on or off for a single company member.

This article explains how to manage MURAL members with the suspend or unsuspend process. Suspension is the most effective (and least disruptive) way to turn off MURAL access at the member level.

> **Note:** When you suspend a member, they cannot log in. If the member is in an active session at the time of suspension, the next action they take will redirect them to the login screen. You can unsuspend a suspended member to turn their access back on.

For example, you could suspend members to streamline your off-boarding process. You could also suspend a list of users who should no longer have system access.

## What is a member?

Members are registered users with full access to features and capabilities that neither guests nor visitors have. They have full collaboration access, have a MURAL profile, and take up a paid product seat. Members can create murals and rooms and invite other members. See Types of Collaborators in MURAL.

From a billing perspective, a user is billable when they access any paid workspaces for three or more days per quarter. If a new member account is suspended before they hit three days of access that quarter, they do not become a billable member.

## What happens when a member is suspended?

When a member is suspended, their ability to log in is disabled, but their existing profile and content is otherwise unaffected.

When a member is suspended:

- They cannot log in or authenticate.
- They cannot access any workspace or content.
- Their number of billable active days is paused.

However, the member is still in the system:

- Their account is visible to other members.
- Their content can be accessed by other members.
- They belong to their previous workspace as inactive members.

## What happens when a member is unsuspended?

When a member is unsuspended (made active again) the following happens:

- Their login is restored.
- They can't access their previous workspaces and content without workspace administrator approval.
- When they first log in, they are prompted to send an unlock request to the workspace admin. If their account is unlocked, they can access their previous content (if it was not transferred to another member before suspension).
- Their number of billable active days is resumed.

## How suspend and unsuspend work on the backend

MURAL servers use an authentication token with a timeout of 15 minutes. The MURAL client (web browser, application) must sync with the server to authenticate.

The authentication token is checked any time the client connects to the server, such as when the web browser is refreshed. If the client does not connect to the server, the last received token expires in 15 minutes.

### When a member is suspended

When a member is suspended, the server does not grant a new token when the client next connects. This means the member can no longer authenticate by any method, and their account is locked.

When a member account is locked, any attempt to log in fails, and the member is presented with an account suspension message, like this one:

<!-- Screenshot omitted: account suspension message shown to a locked-out member -->

### When a member is unsuspended

Unsuspend works differently. The unsuspend command immediately tells the server to grant a valid authentication token the next time the client connects. The member account is unlocked and the next authentication attempt results in success.

## Suspend and unsuspend examples

> **Note:** How to use these examples
>
> Each use case below contains an example using the MURAL Developer Portal API Reference.
>
> Along with the walkthrough steps, you can click the tabs at the top of the example window to view sample API request code in different languages.
>
> You'll need to use a valid API key to follow these examples and generate a response. See Create API Keys for more information.
>
> These example steps will not generate a 200 response unless the member exists in your MURAL account. (And unless you know Luke or Vader, that's probably not true.)

> **Important:** If you attempt to suspend the last admin in a workspace, you will receive a 409 error. One workaround for this is to add an additional admin to your workspace. See Current SCIM limitations.

### Example: Suspend a member account

After the Battle of Endor, Darth Vader is no longer a member of our Galactic Empire company, so we'll turn off his MURAL access.

Let's suspend (deactivate) access for the company member matching the specified email address vader@empire.gov.

**Test this example**

1. On the left of the API Reference, click SCIM protocol > Update an existing company member.
2. Next to the Try It button, click the authentication icon.
3. In the Authorization box, enter apikey followed by a space and your API key.
4. In the userId box, enter vader@empire.gov.
5. For the schemas parameter, select urn:ietf:params:scim:api:messages:2.0:PatchOp from the drop-down.
6. For the Operations parameter, do the following:
   1. op: Select replace from the drop-down.
   2. path: Enter active.
   3. value: Enter false.
7. Click Try It.

**Example request**

The request in cURL would look like this:

```bash
curl --request PATCH \
     --url https://api.mural.co/enterprise/v1/scim/Users/vader%40empire.gov \
     --header 'Accept: application/scim+json' \
     --header 'Authorization: apikey ABCDEFGHIJKLMNOPQRSTUVWXYZ' \
     --header 'Content-Type: application/scim+json' \
     --data '
{
     "schemas": [
          "urn:ietf:params:scim:api:messages:2.0:PatchOp"
     ],
     "Operations": [
            {
                "op": "replace",
                "path": "active",
                "value": "false"
            }
        ]
}
'
```

**Example response**

A 200 response in JSON looks like the code below. Note that active is false. Adiós, Vader.

```json
{
       "active": false,
       "email": [
           {
               "primary": true,
               "value": "vader@empire.gov"
           }
       ],
       "id": "udf4297df66b9aa4b6a856182",
       "userName": "vader@empire.gov",
       "name": {
           "familyName": "Skywalker",
           "givenName": "Anakin"
       },
       "meta": {
           "created": "1977-05-25T18:59:57.913Z",
           "lastModified": "2021-05-26T15:22:51.022Z",
           "resourceType": "User"
       },
       "schemas": [
           "urn:ietf:params:scim:schemas:core:2.0:User"
       ]
}
```

### Example: Unsuspend a member account

Luke Skywalker was temporarily removed from active duty (poor womp-rat performance). However, Princess Leia has welcomed him back, so we'll reinstate his MURAL access.

Let's unsuspend (reactivate) access for the company member matching the email address luke@rebels.org.

**Test this example**

1. On the left of the API Reference, click SCIM protocol > Update an existing company member.
2. Next to the Try It button, click the authentication icon.
3. In the Authorization box, enter apikey followed by a space and your API key.
4. In the userId box, enter luke@rebels.org.
5. For the schemas parameter, select urn:ietf:params:scim:api:messages:2.0:PatchOp from the drop-down.
6. For the Operations parameter, do the following:
   1. op: Select replace from the drop-down.
   2. path: Enter active.
   3. value: Enter true.
7. Click Try It.

**Example request**

The request in cURL looks like this:

```bash
curl --request PATCH \
     --url https://api.mural.co/enterprise/v1/scim/Users/luke%40rebels.org \
     --header 'Accept: application/scim+json' \
     --header 'Authorization: apikey ABCDEFGHIJKLMNOPQRSTUVWXYZ' \
     --header 'Content-Type: application/scim+json' \
     --data '
{
     "schemas": [
          "urn:ietf:params:scim:api:messages:2.0:PatchOp"
     ],
     "Operations": [
          {
               "op": "replace",
               "path": "active",
               "value": "true"
          }
     ]
}
'
```

**Example response**

A 200 response in JSON looks like the code below. Note that active is now true. Welcome back, Luke!

```json
{
      "active": true,
      "email": [
          {
              "primary": true,
              "value": "luke@rebels.org"
          }
      ],
      "id": "udf4297df66b9aa4b6a856182",
      "userName": "luke@rebels.org",
      "name": {
          "familyName": "Skywalker",
          "givenName": "Luke"
      },
      "meta": {
          "created": "1977-05-25T18:59:57.913Z",
          "lastModified": "2021-05-26T15:22:51.022Z",
          "resourceType": "User"
      },
      "schemas": [
          "urn:ietf:params:scim:schemas:core:2.0:User"
      ]
}
```

## Summary

Suspending or unsuspending members allows us to quickly change their login access while leaving their profile, content, and workspaces untouched.

From a billing perspective, a user becomes a billable member when they access any paid workspaces for three or more days per quarter. If a new user's account is suspended before they hit three days of access that quarter, they do not become a billable member.

---

*Published help center documentation. Product name and example data appear as originally published.*
