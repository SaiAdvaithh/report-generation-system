import axios from "axios";
import React, { useState, useEffect } from "react";

function ReportGenerator() {

  const [fromDate, setFromDate] = useState("");
  const [toDate, setToDate] = useState("");

  useEffect(() => {
    const now = new Date();
    const oneHourAgo = new Date(now.getTime() - 60 * 60 * 1000);

    const formatLocal = (date) => {
      const offset = date.getTimezoneOffset() * 60000;
      return new Date(date - offset).toISOString().slice(0, 16);
    };

    setFromDate(formatLocal(oneHourAgo));
    setToDate(formatLocal(now));
  }, []);




  const [containerId, setContainerId] = useState("");
  const [companyName, setCompanyName] = useState("");
  const [facilityName, setFacilityName] = useState("");
  const [address, setAddress] = useState("");
  const [reportId, setReportId] = useState("");
  const [auditor, setAuditor] = useState("");
  const [reviewer, setReviewer] = useState("");
  const [approver, setApprover] = useState("");

  const [logo, setLogo] = useState(null);
  const [signature, setSignature] = useState(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const generateReport = async () => {

    // ✅ VALIDATION
    if (
      !containerId || !companyName || !facilityName || !address ||
      !reportId || !auditor || !reviewer || !approver || !logo || !signature
    ) {
      alert("Please fill all fields and upload files");
      return;
    }

    try {
      setLoading(true);
      setError("");

      const formData = new FormData();

      // 🔥 TEXT FIELDS
      formData.append("company_name", companyName);
      formData.append("facility_name", facilityName);
      formData.append("address", address);
      formData.append("report_id", reportId);
      formData.append("auditor", auditor);
      formData.append("reviewer", reviewer);
      formData.append("approver", approver);

      formData.append("from_date", new Date(fromDate).toISOString());
      formData.append("to_date", new Date(toDate).toISOString());

      // 🔥 FILES
      formData.append("logo", logo);
      formData.append("signature", signature);

      const response = await axios.post(
        `http://127.0.0.1:8000/report/${containerId}`,
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
          responseType: "blob",
        }
      );

      // 🔥 DOWNLOAD PDF
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");

      link.href = url;
      link.setAttribute("download", `container_${containerId}.pdf`);

      document.body.appendChild(link);
      link.click();

      // ✅ RESET FORM
      setContainerId("");
      setCompanyName("");
      setFacilityName("");
      setAddress("");
      setReportId("");
      setAuditor("");
      setReviewer("");
      setApprover("");
      setLogo(null);
      setSignature(null);

      setLoading(false);

    } catch (err) {
      console.error("FULL ERROR:", err);

      if (err.response) {
        console.error("BACKEND ERROR:", err.response.data);
        setError(JSON.stringify(err.response.data));
      } else {
        setError("Server not reachable");
      }

      setLoading(false);
    }
  };

  return (
    <div style={{ padding: 40 }}>
      <h2>Container Report Generator</h2>

      {error && <p style={{ color: "red" }}>{error}</p>}
      <p>Report Date Range</p>
      
      <p> From:</p>
      <input
        type="datetime-local"
        value={fromDate}
        onChange={(e) => setFromDate(e.target.value)}
      />
      <p> To:</p>
      <input
        type="datetime-local"
        value={toDate}
        onChange={(e) => setToDate(e.target.value)}
      />


      <br /><br />
      <input
        placeholder="Container ID"
        value={containerId}
        onChange={(e) => setContainerId(e.target.value)}
      />

      <br /><br />

      <input
        placeholder="Company Name"
        value={companyName}
        onChange={(e) => setCompanyName(e.target.value)}
      />

      <br /><br />
      
      <input
        placeholder="Facility Name"
        value={facilityName}
        onChange={(e) => setFacilityName(e.target.value)}
      />

      <br /><br />

      <input
        placeholder="Address"
        value={address}
        onChange={(e) => setAddress(e.target.value)}
      />

      <br /><br />

      <input
        placeholder="Report ID"
        value={reportId}
        onChange={(e) => setReportId(e.target.value)}
      />

      <br /><br />

      <input
        placeholder="Auditor"
        value={auditor}
        onChange={(e) => setAuditor(e.target.value)}
      />

      <br /><br />

      <input
        placeholder="Reviewer"
        value={reviewer}
        onChange={(e) => setReviewer(e.target.value)}
      />

      <br /><br />

      <input
        placeholder="Approver"
        value={approver}
        onChange={(e) => setApprover(e.target.value)}
      />

      <br /><br />
        
      <p>Add Logo</p>
      <input
        type="file"
        onChange={(e) => setLogo(e.target.files[0])}
      />
      {logo && <p>Logo: {logo.name}</p>} 

      <br />
      <p>Signature</p>
      <input
        type="file"
        onChange={(e) => setSignature(e.target.files[0])}
      />
      {signature && <p>Signature: {signature.name}</p>}
      
      <br /><br />

      <button onClick={generateReport} disabled={loading}>
        {loading ? "Generating..." : "Generate Report"}
      </button>
    </div>
  );
}

export default ReportGenerator;