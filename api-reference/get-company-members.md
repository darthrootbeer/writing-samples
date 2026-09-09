---
title: Get Company Members
type: API guide
original_format: PDF (published help center article)
---

# Get Company Members

How to use the company members endpoint to retrieve member information.

The company members endpoint retrieves the name, email address, and other details for a member of your company using the parameters you choose.

## Parameters

You can use one or more than one parameter at a time.

| Parameter | Description | Use case |
|---|---|---|
| `email` | Find out the name of a member who has a specific email address. | Find a member with the email address `jdoe@company.com`. |
| `locked` | Find out which members are active or deactivated. A deactivated member cannot log into the system and, therefore, cannot access anything. To do this, enter true for active members and false for deactivated members. | Find deactivated members. |
| `maxInteractions` | Find out which members have accessed the company's MURAL account no more than a specified number of times in the last three months. | Find members who have accessed the company's MURAL account at most four times in the last three months. |
| `minInteractions` | Find out which members have accessed the company's MURAL account no less than a specified number of times in the last three months. | Find members who have accessed the company's MURAL account at least five times in the last three months. |
| `lastSeenAfter` | Find out which members have logged in after a date that you specify. Use the date format, YYYY-MM-DD. | Find members who have logged in after October 19, 2020. |
| `lastSeenBefore` | Find out which members have logged in before a date that you specify. Use the date format, YYYY-MM-DD. | Find members who have logged in before December 3, 2020. |
| `organic` | Find out which members were brought into MURAL via an invitation link (organic members) and which members were added by admins (non-organic members). | Find organic members. |

## Testing the company members endpoint

> **Note:** How to use these examples
>
> Each use case below contains an example using the MURAL Developer Portal API Reference.
>
> Along with the walkthrough steps, you can click the tabs at the top of the example window to view the generated code in different languages. You'll find example code in cURL, Node, Ruby, Javascript, and Python.
>
> Note: You'll need to use a valid API key to follow these examples and generate a response. See Create API Keys for more information.

### Example: Getting a company member by email

Get company members with a specific email address.

**Test this example**

1. In the API Reference, click Deprovisioning > Get a list of company members on the left.
2. Next to the Try It button, click the authentication icon.
3. In the Authorization box, enter apikey followed by a space and your API key.
4. In the email field, enter the email address you want to use.
5. Click Try It.

The API generates a server response of 200 OK with additional JSON output. Click the sections to expand or collapse them.

The results show the data for any member matching the specified email address. Here is an example of those results, as shown with JSON formatting.

```json
{
    "results":[
      {
        "email":"dblake@avengers.co",
        "name":"Donald",
        "surname":"Blake",
        "type":null
      }
    ]
}
```

### Example: Getting company members seen within a date range

Get company members who have been in the system within a specific date range.

**Test this example**

1. In the API Reference, click Deprovisioning > Get a list of company members on the left.
2. Next to the Try It button, click the authentication icon.
3. In the Authorization box, enter apikey followed by a space and your API key.
4. In the lastSeenAfter field, enter a start date. Use the date format, YYYY-MM-DD.
5. In the lastSeenBefore field, enter an end date. Again, use the date format, YYYY-MM-DD.
6. Click Try It.

The API generates a server response of 200 OK with additional JSON output. Click the sections to expand or collapse them.

The results will show the names of members who were in the system within the date range you specified. Here is an example of those results.

```json
{
    "results": [
        {
          "email": "aking@company.co",
          "name": "Ann",
          "surname": "King",
          "type": null
      },
      {
          "email": "psmith@company.co",
          "name": "Peter",
          "surname": "Smith",
          "type": null
      }
    ]
}
```

### Example: Getting a list of QEMs

Quarterly Engaged Members (QEMs) are a specific type of company member. Here are the qualifications for being a QEM:

- They are an internal member, meaning a member that is an employee at the company that is paying for the workspace.
- They have done something inside a workspace room or mural on at least three different days within the last 90 days.

You can use this endpoint to find out if a member is a QEM. Here's how:

1. In the API Reference, click Deprovisioning > Get a list of company members on the left.
2. Next to the Try It button, click the authentication icon.
3. In the Authorization box, enter apikey followed by a space and your API key.
4. In the minInteractions field, enter 3.
5. Click Try It.

The API generates a Request URL and a Server response of 200. The results will show the names of members who qualify as QEMs. Here is an example of those results, as shown with JSON formatting.

```json
{
    "results": [
        {
             "email": "jmills@company.co",
             "name": "Jane",
             "surname": "Mills",
             "type": null
        },
        {
             "email": "rclark@company.co",
             "name": "Rose",
             "surname": "Clark",
             "type": null
        }
    ]
}
```

---

*Published help center documentation. Product name and example data appear as originally published.*
