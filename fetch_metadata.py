import requests
import xml.etree.ElementTree as ET
import json

assembly_accession = 'GCA_000696205.1'

esearch_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'
elink_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi'
efetch_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi'
esummary_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi'

payload_search = {
    'db': 'assembly',
    'term': '{}[asac]'.format(assembly_accession),
    'usehistory': 'y'
}
r = requests.get(esearch_url, params=payload_search)

root = ET.fromstring(r.text)

query_key = root.find('QueryKey').text
web_env = root.find('WebEnv').text
assembly_uid = root.find('IdList').find('Id').text

payload_assembly = {
    'db': 'assembly',
    'WebEnv': web_env,
    'query_key': query_key,
    'retmode': 'json'
}
r = requests.get(esummary_url, params=payload_assembly)

# assembly data
print(r.text)

assembly = json.loads(r.text)
bioproject_id = assembly['result'][assembly_uid]['gb_bioprojects'][0]['bioprojectid']
biosample_id = assembly['result'][assembly_uid]['biosampleid']

payload_bioproject = {
    'db': 'bioproject',
    'id': bioproject_id,
    'retmode': 'json'
}
r = requests.get(esummary_url, params=payload_bioproject)

# bioproject data
print(r.text)

payload_biosample = {
    'db': 'biosample',
    'id': biosample_id,
    'retmode': 'json'
}
r = requests.get(esummary_url, params=payload_biosample)

# biosample data
print(r.text)

payload_elink = {
    'db': 'genome',
    'WebEnv': web_env,
    'query_key': query_key,
    'retmode': 'json'
}
r = requests.get(elink_url, params=payload_elink)
print(r.text)
genome_uid = json.loads(r.text)['linksets'][0]['linksetdbs'][0]['links'][0]

payload_genome = {
    'db': 'genome',
    'id': genome_uid,
    'retmode': 'json'
}
r = requests.get(esummary_url, params=payload_genome)

# genome data
print(r.text)
