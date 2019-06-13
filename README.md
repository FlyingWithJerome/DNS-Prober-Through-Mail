## DNS Prober Through Mail Infrastructure

#### Method

This prober sends mails to a non-existing user in a domain, which will trigger a Delivery Status Notification (DSN). Thus the prober forces the domain's private DNS resolver to query a specified ADNS (to query the MX record of the sender so that the DSN can be sent back).

#### IMPORTANT

Use this prober PROPERLY. Do NOT use this prober to flood others' mail servers. Carefully think about INTERNET ETHICS before use.