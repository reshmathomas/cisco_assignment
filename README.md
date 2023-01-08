# Malware URL lookup exercise

## Overview
This repo consists of a basic web service written using Python and the Flask framework which checks whether the given URL is
a malware or not by checking whether the URL exists in the malware_urls.malware_url_info table on the host.

## Functional Requirements
1. Parse the GET request consisting of a URL
2. Check the database of malware URLs to identify whether the given URL is a malware
3. Return JSON response {'url':<url>,'malware':True/False}

## Non-functional requirements
1. Highly scalable
2. Low latency
3. Highly available

## Resource estimation

### Assumptions
1. URL length does not exceed 512 bytes in length
2. The URL passed to the service must be in a proper format, i.e,
<protocol>://subdomain.secondlevel-domain.tld else an error is returned

### Given
2. Number of write requests = approx. 5000 URLs a day
3. Period for updates to the database = every 10 minutes
4. Number of reads is much greater than number of writes to the database

## Design for non-functional requirements

## High-level components and design decisions
1. Clients interface first with a highly available load-balancer to distribute read/write requests to a fleet of horizontally scaled web servers. To use this service globally, the load balancer also has the capability to perform geo-routing to servers distributed across the globe.
2. Fleet of horizontally scaled statless web servers across racks, datacenters and regions to ensure high availability which perform lookup of URLs in the database. The web service is deployed in containers such as Kubernetes so as to easily scale and make available.
3. Horizontally scaled cache servers such as a Redis cluster or a CDN such as Amazon CloudFront if the service is used globally. This is because the reads are expected to be much greater than writes. URL information being static data can be easily cached, thus reducing the load on storage servers and reducing latency for read requests.
4. Distributed NoSQL database to be able to store as many URLs as required. Even though the relational databases can be used to efficiently lookup URLs, these can be difficult to scale. Hence, the use of a NoSQL database is preferred here.
	4.1. Choice of NoSQL database - If eventual consistency is acceptable, Redis is preferred here since it can be used as an in-memory cache and a database. Therefore, the caching layer can be combined with the data storage layer. If strong consistency is required, Mongo DB is preferred here but will result in a few seconds of downtime for leader election as it is deployed as primary-secondary servers. MongoDB also has concurrency control protocols, thus handling concurrent reads and writes to the database.
	4.2 Data stored in the database: Currently, the hostname extracted from the URL is stored as is. This is to treat a URL with and without https the same. However, a way to deal with URLs longer than 512 bytes are to hash the URL and use the hash as the primary index.

## System APIs
1. GET /v1/urlinfo/{url} (Implemented)
Returns a JSON response of the form {'url':<url>,'malware':True/False}

2. POST /v1/urlinfo/add/{url} (Not implemented)
Adds new URLs to the malware_url_info table.
Ignores the request if url is already present in the table
Returns a JSON response {'url':<url>,'status':<SUCCESS/FAILURE>,'errcode': empty/errcode for database insert}

## System usage

### Pre-requisites:
1. Python2+
2. pip
3. MySQL server

1. Install the following dependencies using pip:
- Flask
- mysqlclient

Note: Installing MySQL and client on MacOS can be tricky. Recommend following the steps in https://ruddra.com/install-mysqlclient-macos/

2. Download the files in the app/ folder and run the app using:
`python app.py`
This creates the database and malware_url_info table. Insert few fake URLs in the table as follows:
`INSERT INTO malware_url_info values("www.fakeurl.com");`

3. Send a GET request to the web service that runs on localhost:105 by typing in the following in a browser:
`http://localhost:105/v1/urlinfo/?url=https://www.fakeurl.com`

4. Run the tests from the parent directory using the command: `python -m tests.test_malware_url_lookup_db`
