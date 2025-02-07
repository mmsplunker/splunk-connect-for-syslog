import random

from jinja2 import Environment

from .sendmessage import *
from .splunkutils import *
from .timeutils import *
import pytest

env = Environment()

testdata_mcafee_nsp_audit = [
    '{{ mark }} {{ bsd }} {{ host }} {{ app }}: audit_action="Audit Syslog Forwarder Message Customization" audit_result="succeeded" audit_time="2020-12-28 18:23:36 UTC" user="Administrator" category="Admin Domain" audit_domain="My Company" detail_comment="N/A" detail_delta="N/A"'
]
testdata_mcafee_nsp_alert = [
    '{{ mark }} {{ bsd }} {{ host }} {{ app }}: domain="My Company" alertid="6845473495895750289" alert_type="Statistical Anomaly" app_protocol="N/A" confidence="N/A" attack_count="1" attackid="Ox40008200" attack_name="Inbound UDP Packet Volume Too High" severity="High" alert_signature="N/A" attack_time="2020-12-28 19:08:26 UTC" category="VolumeDos" dest_ip="N/A" dest_name="N/A" dest_port="N/A" device_name="Mcafee_ips" direction="Inbound" confidence="N/A" file_name="N/A" file_hash="N/A" file_type="N/A" virus_name="N/A" action_status="Unknown" error_status="No error" protocol="N/A" result="n/a" src_ip="N/A" src_name="N/A" src_port="N/A" alert_uuid="2669053482585045088"'
]
testdata_mcafee_nsp_acl = [
    '{{ mark }} {{ bsd }} {{ host }} {{ app }}: acl_action="PERMIT" description="" policy="Test Firewall Policy" rule_id="1" admin_domain="My Company" alert_count="N/A" direction="Inbound" duration="N/A" application="N/A" app="N/A" dest_country="N/A" dest_hostname="N/A" dest_ip="10.160.29.34" dest_port="514" interface="1-2" acl_protocol="udp" sensor_name="Mcafee_ips" src_country="N/A" src_host="N/A" src_ip="10.160.0.2" src_port="32825" user="N/A"'
]
testdata_mcafee_nsp_fault = [
    '{{ mark }} {{ bsd }} {{ host }} {{ app }}: Fault : dvc="Manager" description="The Manager is unable to connect to the McAfee Update Server." ack_information="" additional_text="The Manager is unable to connect to the McAfee Update Server." admin_domain="My Company:" fault_component="UpdateServer" fault_level="Manager system level" fault_name="Update Server Connectivity Error" fault_source="Generated by Manager" fault_time="2020-12-28 18:26:57 UTC" fault_type="cleared" member_device="N/A" owner_id="0" recommended_action="Consult the system log for details and confirm that the Manager can resolve names and communicate with its default gateway and proxy server, as applicable." severity="Critical"'
]


@pytest.mark.parametrize("event", testdata_mcafee_nsp_audit)
def test_mcafee_nsp_audit(
    record_property, setup_wordlist, setup_splunk, setup_sc4s, event
):
    host = "mcafee-nsp"
    dt = datetime.datetime.now()
    iso, bsd, time, date, tzoffset, tzname, epoch = time_operations(dt)

    epoch = epoch[:-7]

    mt = env.from_string(event + "\n")
    message = mt.render(mark="<36>", bsd=bsd, host=host, app="SyslogAuditLogForwarder")

    sendsingle(message, setup_sc4s[0], setup_sc4s[1][514])

    st = env.from_string(
        'search index=netids _time={{ epoch }} host={{ host }} sourcetype="mcafee:nsp" _raw="{{ message }}"'
    )

    message1 = mt.render(mark="", bsd="", host="", app="")
    search = st.render(
        epoch=epoch, host=host, message=message1.lstrip().replace('"', '\\"')[2:]
    )
    print("search:", search)
    resultCount, eventCount = splunk_single(setup_splunk, search)

    record_property("host", host)
    record_property("resultCount", resultCount)
    record_property("message", message)

    assert resultCount == 1


@pytest.mark.parametrize("event", testdata_mcafee_nsp_alert)
def test_mcafee_nsp_alert(
    record_property, setup_wordlist, setup_splunk, setup_sc4s, event
):
    host = "mcafee-nsp"
    dt = datetime.datetime.now()
    iso, bsd, time, date, tzoffset, tzname, epoch = time_operations(dt)

    epoch = epoch[:-7]

    mt = env.from_string(event + "\n")
    message = mt.render(mark="<36>", bsd=bsd, host=host, app="SyslogAlertForwarder")

    sendsingle(message, setup_sc4s[0], setup_sc4s[1][514])

    st = env.from_string(
        'search index=netids _time={{ epoch }} host={{ host }} sourcetype="mcafee:nsp" _raw="{{ message }}"'
    )

    message1 = mt.render(mark="", bsd="", host="", app="")
    search = st.render(
        epoch=epoch, host=host, message=message1.lstrip().replace('"', '\\"')[2:]
    )
    print("search:", search)
    resultCount, eventCount = splunk_single(setup_splunk, search)

    record_property("host", host)
    record_property("resultCount", resultCount)
    record_property("message", message)

    assert resultCount == 1


@pytest.mark.parametrize("event", testdata_mcafee_nsp_acl)
def test_mcafee_nsp_acl(
    record_property, setup_wordlist, setup_splunk, setup_sc4s, event
):
    host = "mcafee-nsp"
    dt = datetime.datetime.now()
    iso, bsd, time, date, tzoffset, tzname, epoch = time_operations(dt)

    epoch = epoch[:-7]

    mt = env.from_string(event + "\n")
    message = mt.render(mark="<36>", bsd=bsd, host=host, app="SyslogACLLogForwarder")

    sendsingle(message, setup_sc4s[0], setup_sc4s[1][514])

    st = env.from_string(
        'search index=netids _time={{ epoch }} host={{ host }} sourcetype="mcafee:nsp" _raw="{{ message }}"'
    )

    message1 = mt.render(mark="", bsd="", host="", app="")
    search = st.render(
        epoch=epoch, host=host, message=message1.lstrip().replace('"', '\\"')[2:]
    )
    print("search:", search)
    resultCount, eventCount = splunk_single(setup_splunk, search)

    record_property("host", host)
    record_property("resultCount", resultCount)
    record_property("message", message)

    assert resultCount == 1


@pytest.mark.parametrize("event", testdata_mcafee_nsp_fault)
def test_mcafee_nsp_fault(
    record_property, setup_wordlist, setup_splunk, setup_sc4s, event
):
    host = "mcafee-nsp"
    dt = datetime.datetime.now()
    iso, bsd, time, date, tzoffset, tzname, epoch = time_operations(dt)

    epoch = epoch[:-7]

    mt = env.from_string(event + "\n")
    message = mt.render(mark="<36>", bsd=bsd, host=host, app="SyslogFaultForwarder")

    sendsingle(message, setup_sc4s[0], setup_sc4s[1][514])

    st = env.from_string(
        'search index=netids _time={{ epoch }} host={{ host }} sourcetype="mcafee:nsp" _raw="{{ message }}"'
    )

    message1 = mt.render(mark="", bsd="", host="", app="")
    search = st.render(
        epoch=epoch, host=host, message=message1.lstrip().replace('"', '\\"')[2:]
    )
    print("search:", search)
    resultCount, eventCount = splunk_single(setup_splunk, search)

    record_property("host", host)
    record_property("resultCount", resultCount)
    record_property("message", message)

    assert resultCount == 1
