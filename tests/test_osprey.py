import json, sys, tempfile, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from osprey.charter import Charter
from osprey.actions import Proposal, ActionClass
from osprey.audit import AuditLedger
from osprey.killswitch import KillSwitch
from osprey.tools import webshield, integrity, secrets as st
from osprey.agents import CARDS

CH = Charter(owner="Matthew", hosts=["example.com"], docroots=["/tmp"], signed_by="Matthew")

class TestCharter(unittest.TestCase):
    def test_enrolled_and_refused(self):
        self.assertTrue(CH.is_enrolled_url("https://example.com/page"))
        self.assertFalse(CH.is_enrolled_url("https://victim.example/page"))
    def test_unsigned_is_invalid(self):
        self.assertIn("signed_by", " ".join(Charter(owner="x", hosts=["a.com"]).validate()))

class TestActions(unittest.TestCase):
    def test_a1_auto_only_high_low_collateral(self):
        self.assertTrue(Proposal(ActionClass.A1, "ttl block", 0.95, 0.005).auto_allowed())
        self.assertFalse(Proposal(ActionClass.A1, "ttl block", 0.5, 0.005).auto_allowed())
    def test_a4_never_auto(self):
        self.assertFalse(Proposal(ActionClass.A4, "wipe", 1.0, 0.0).auto_allowed())

class TestAudit(unittest.TestCase):
    def test_chain_verifies_and_tamper_breaks(self):
        with tempfile.TemporaryDirectory() as d:
            led = AuditLedger(Path(d) / "audit.jsonl")
            led.append({"kind": "proposal", "id": "1"}); led.append({"kind": "verdict", "id": "1"})
            self.assertTrue(led.verify())
            lines = Path(led.path).read_text().splitlines(); lines[0] = lines[0].replace("proposal", "tampered")
            Path(led.path).write_text("\n".join(lines) + "\n"); self.assertFalse(led.verify())

class TestWebshield(unittest.TestCase):
    def test_missing_headers_flagged(self):
        r = {x["check"]: x["status"] for x in webshield.check_headers({"Server": "nginx"})}
        self.assertEqual(r["header:strict-transport-security"], "fail")
    def test_upload_form_found(self):
        html = '<form action="/up.php" method="post"><input type="file" name="f"></form>'
        self.assertEqual(webshield.find_upload_forms(html)[0]["action"], "/up.php")
    def test_magento_cve_range(self):
        self.assertTrue(webshield.check_magento("2.4.7")["affected"])
        self.assertFalse(webshield.check_magento("2.4.10")["affected"])
    def test_webshell_and_secrets(self):
        self.assertTrue(webshield.scan_text_for_webshell("eval($_POST['x'])"))
        self.assertIn("aws_key", st.scan_text("AKIAIOSFODNN7EXAMPLE"))
    def test_panel_refuses_nonenrolled(self):
        self.assertEqual(webshield.check_exposed_panel("https://other.com:8000", CH)["status"], "refused")

class TestAgents(unittest.TestCase):
    def test_reader_is_toolless(self):
        self.assertTrue(CARDS["reader"].toolless)
        self.assertEqual(CARDS["reader"].tools, ())

if __name__ == "__main__":
    unittest.main()
