'''
mx_query.py

query the mx record for the domain name
'''
import dns.resolver

def query_mx_record(domain_name: str) -> [(int, str),]:
    '''
    query the mx record, return a list of sorted
    (preference, mx name) pair by preference
    '''
    mx_record_list = []
    for mx_record in dns.resolver.query(domain_name, rdtype=dns.rdatatype.MX):
        preference, mx_answer = mx_record.to_text().split(" ")
        mx_record_list.append((int(preference), mx_answer))
    mx_record_list.sort(key=lambda x: x[0], reverse=True)
    return mx_record_list

if __name__ == "__main__":
    query_mx_record("case.edu")
