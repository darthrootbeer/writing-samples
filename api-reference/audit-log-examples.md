---
title: Audit Log Examples
type: API guide
original_format: PDF (published help center article)
---

# Audit Log Examples

Testing the audit logs endpoint, with examples.

The audit logs endpoint provides detailed logging information and large amounts of data. The following examples step through some audit logs use cases to explain how the parameters function.

> **Note:** How to use these examples
>
> Each use case below contains an example using the MURAL Developer Portal API Reference.
>
> Along with the walkthrough steps, you can click the tabs at the top of the example window to view the generated code in different languages. You'll find example code in cURL, Node, Ruby, Javascript, and Python.
>
> Note: You'll need to use a valid API key to follow these examples and generate a response. See Create API Keys for more information.

## Limit results to a specific number of entries

By default, the audit logs endpoint provides the most log entries, up to 1000 per response. But, we can limit responses to get manageable results.

The maxResults parameter returns the specified number of audit log entries in the response. Valid maxResults requests are 1–1000.

> **Note:** To retrieve more than 1000 entries, we use nextToken to paginate responses across multiple requests. See Use tokens to request additional data.

### Example: Retrieve last 50 entries

By setting maxResults to 50, we retrieve only the latest 50 entries.

**Example request**

```bash
curl --request GET \
     --url 'https://api.mural.co/enterprise/v1/audit-log?maxResults=50' \
     --header 'Accept: application/json' \
     --header 'Authorization: apikey YOURAPIKEY'
```

**Example response**

```json
{
    "data": [
       {
         "action": "UPDATE_COMPANY_SSO",
         "actor": {
            "company": "MURAL",
            "email": "exampleemail@mural.co",
            "id": "exampleId",
            "name": "Integrations Example User",
            "type": "USER"
          },
         "date": "2022-02-01 22:19:42.841",
         "id": "node-8ae0c784e3e11697b0850c80129ad26b-44d3386d-788e-4da4-9afa-2814cb54cd12",
         "ip": "126.33.94.213",
         "affected": {
            "company": "muraltestenterprise",
            "id": "muraltestenterprise",
            "type": "COMPANY"
          }
       },
       // additional 49 records
    ],
    "nextToken": "eyJleGVjdXRpb25...BUm9vMVVRPT0ifQ=="
}
```

**Test this example**

1. In the API Reference, click Audit Logs on the left.
2. Scroll down to the "Try It" section.
3. Next to the Try It button, click the authentication icon.
4. In the Authorization box, enter apikey followed by a space and your API key.
5. In the maxResults field, enter 50.
6. Click Try It.

The API generates a server response of 200 OK with additional JSON output. Click the sections to expand or collapse them.

You should see 50 audit log entries in the response data.

## Filter results by date

Use the filter[date][since] and filter[date][until] parameters to limit the response to a specific date range.

Dates are in UTC timezone, and use the format (yyyy-mm-dd HH:mm:ss).

### Example: Only show entries since a certain date

Here, we can limit the results to only show actions starting on a certain date.

**Example request**

```bash
curl --request GET \
     --url 'https://api.mural.co/enterprise/v1/audit-log?filter[date][since]=2022-01-01' \
     --header 'Accept: application/json' \
     --header 'Authorization: apikey YOURAPIKEY'
```

**Test this example**

1. In the API Reference, click Audit Logs on the left.
2. Scroll down to the "Try It" section.
3. Next to the Try It button, click the authentication icon.
4. In the Authorization box, enter apikey followed by a space and your API key.
5. In the filter[date][since] field, enter a start date.
6. Click Try It.

The API generates a server response of 200 OK with additional JSON output. Click the sections to expand or collapse them.

Verify the earliest entry in the response (at the bottom) matches your since date. Remember, audit logs display in reverse chronological order, and contain up to 30 days of entries. If you don't define a specific time range using the filter[date][since] and filter[date][until] fields, the API returns events from the past 7 days. Over 120 events can be logged.

### Example: Only show entries within a date range

Let's show entries between two dates. We'll use both filter[date][since] and filter[date][until] to achieve this.

Responses are limited to a maximum range of 30 days. If you don't define a specific time range using the filter[date][since] and filter[date][until] fields, the API returns events from the past 7 days.

**Example request**

```bash
curl --request GET \
     --url 'https://api.mural.co/enterprise/v1/audit-log?filter[date][since]=2022-01-01' \
     --header 'Accept: application/json' \
     --header 'Authorization: apikey YOURAPIKEY'
```

**Test this example**

1. In the API Reference, click Audit Logs on the left.
2. Scroll down to the "Try It" section.
3. Next to the Try It button, click the authentication icon.
4. In the Authorization box, enter apikey followed by a space and your API key.
5. In the filter[date][since] field, enter a start date.
6. In the filter[date][until] field, enter a end date.
7. Click Try It.

The API generates a server response of 200 OK with additional JSON output. Click the sections to expand or collapse them.

Verify that the entry at the top of the output is no later than your until date. The last entry in the output should be no earlier than your since date. Remember, audit logs display in reverse chronological order, and contain up to 30 days of entries. If you don't define a specific time range using the filter[date][since] and filter[date][until] fields, the API returns events from the past 7 days.

## Use tokens to request additional data

The response limit is 1,000 entries. To retrieve more than 1,000 sequential results, we can use the nextToken parameter to paginate responses across a few requests.

### What is a token?

Every audit logs response concludes with a token. A token is a long string of characters that serves as a unique bookmark to our current result set.

Tokens appear at the very end of every audit logs response, and look like this:

```
"nextToken": "eyJfi0TPn9mT4AHWqtCR...CZJ52bpRXdjVGelQ=="
```

### How does a token work?

Think of using a token like placing a marker. We use this imaginary marker every 1,000 pages to locate request "the next 1000 pages" of information.

By using this token in our next API call, the API remembers where the last response ended. It continues its response to our previous request, starting with the next set of data. And it puts a token at the end of the new request, in case we'd like to continue even further.

### Example: Use a token to paginate large responses

What if we want to retrieve much more than 1,000 results?

In this first example, we'll do a simple audit log dump, and take everything we can. Well, up to three requests worth of data, anyway—around 3,000 entries.

**Example request**

```bash
curl --request GET \
     --url 'https://api.mural.co/enterprise/v1/audit-log?maxResults=1000&nextToken=eyJl...' \
     --header 'Accept: application/json' \
     --header 'Authorization: apikey YOURAPIKEY'
```

**Test this example**

1. In the API Reference, click Audit Logs on the left.
2. Scroll down to the "Try It" section.
3. Next to the Try It button, click the authentication icon.
4. In the Authorization box, enter apikey followed by a space and your API key.
5. Clear all fields.
6. Click Try It.

The API generates a server response of 200 OK with additional JSON output. Click the sections to expand or collapse them.

At the end of the response, we are provided with a token:

```
"nextToken": "eyJfi0TPn9mT4AHWqt...HRqhUQVJjcDticz5=="
```

We'll use this token in our next sequential API call to continue the responses where we left off.

**To continue the previous response**

1. At the end of the previous response output, locate the token.
2. Copy the token, excluding the start and end quotes.
3. In the nextToken field, paste the token.
4. Click Try It.

At the end of this second response is another token, which can use in a third request to pull down the third set of data. And so on, and so forth.

> **Note:** Any fields other than maxResults are ignored when we use a nextToken field.

### Example: Use a token to paginate smaller response sets

We can also use tokens to continue parsing smaller sets of data.

For example, if we want to view every time the ACCEPT_MEMBERSHIP action occurred, but limit our responses to sets of 25, we can do so using tokens.

Here, we can show all ACCEPT_MEMBERSHIP entries, 25 at a time.

**Test this example**

1. In the API Reference, click Audit Logs on the left.
2. Scroll down to the "Try It" section.
3. Next to the Try It button, click the authentication icon.
4. In the Authorization box, enter apikey followed by a space and your API key.
5. In the maxResults field, enter 25.
6. In the filter[action] field, enter the action ACCEPT_MEMBERSHIP.
7. Click Try It.

The API generates a server response of 200 OK with additional JSON output. Click the sections to expand or collapse them.

At the end of the response, we are provided with a token that looks something like this:

```
"nextToken": "eyJleGVjdXRpb25...BUm9vMVVRPT0ifQ=="
```

We'll use this token from response with the first 25 results set to continue with another 25 results from the same set.

**To continue the previous response**

1. At the end of the previous response output, locate the token.
2. Copy the token, excluding the start and end quotes.
3. In the nextToken field, paste the token.
4. Click Try It.

> **Note:** Any fields other than maxResults are ignored when we use a nextToken field.

## Filter results by action

Each entry in the audit log is an action and the action's details.

As you can imagine, there are many available actions in an audit log. If we know what we're looking for, we can filter by a specific action to show only the log entries with that action. We can filter by one action at a time.

### Example: Show all events where a new mural was created

First, we'll request audit log entries for the action CREATE_MURAL. Since we aren't setting a specific time range using the filter[date][since] and filter[date][until] fields, the API returns events from the past 7 days.

**Example request**

```bash
curl --request GET \
     --url 'https://api.mural.co/enterprise/v1/audit-log?filter[action]=CREATE_MURAL' \
     --header 'Accept: application/json' \
     --header 'Authorization: apikey YOURAPIKEY'
```

**Test this example**

1. In the API Reference, click Audit Logs on the left.
2. Scroll down to the "Try It" section.
3. Next to the Try It button, click the authentication icon.
4. In the Authorization box, enter apikey followed by a space and your API key.
5. In the filter[action] field, enter the action CREATE_MURAL.
6. Click Try It.

The API generates a server response of 200 OK with additional JSON output. Click the sections to expand or collapse them.

If you scroll through the response data, you can see that every action is a CREATE_MURAL action.

### Example: Show the last 25 sign-in failures

We can make our results more relevant to what we want to know combining the action filter with maxResults. This test will show us who couldn't sign in, but limit the return to 25 entries.

**Test this example**

1. In the API Reference, click Audit Logs on the left.
2. Scroll down to the "Try It" section.
3. Next to the Try It button, click the authentication icon.
4. In the Authorization box, enter apikey followed by a space and your API key.
5. In the maxResults field, enter 25.
6. In the filter[action] field, enter the action SIGN_IN_FAILURE.
7. Click Try It.

### Example: Show all LEAVE_WORKSPACE events after 1 January, 2021

Let's say we want to know which members left a workspace after the holidays. This test displays all LEAVE_WORKSPACE actions occurring after 1 January, 2021.

**Test this example**

1. In the API Reference, click Audit Logs on the left.
2. Scroll down to the "Try It" section.
3. Next to the Try It button, click the authentication icon.
4. In the Authorization box, enter apikey followed by a space and your API key.
5. In the filter[action] field, enter the action LEAVE_WORKSPACE.
6. In the filter[date][since] field, enter 2021-01-01.
7. Click Try It.

The API generates a server response of 200 OK with additional JSON output. Click the sections to expand or collapse them.

If you scroll through the response data, you can see that every action is a LEAVE_WORKSPACE action, with the date of each action occurring on or after January 1.

---

*Published help center documentation. Product name and example data appear as originally published.*
