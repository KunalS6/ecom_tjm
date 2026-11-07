const page = document.querySelector("#review-page");
const orderId = page.dataset.orderId;
const statusMessage = document.querySelector("#review-status");
const detailsPanel = document.querySelector("#review-details");
const token = window.location.hash.slice(1);

history.replaceState(null, "", window.location.pathname);

async function reviewRequest(action, reason = "") {
  const response = await fetch(`/api/reviews/${orderId}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ action, token, reason }),
  });
  if (!response.ok) {
    const result = await response.json();
    throw new Error(result.error || "This review link is invalid or has expired.");
  }
  return response;
}

function addDetail(label, value) {
  const row = document.createElement("p");
  const heading = document.createElement("strong");
  heading.textContent = `${label}: `;
  row.append(heading, document.createTextNode(value || "—"));
  return row;
}

async function loadReview() {
  if (!token) throw new Error("Open the private review link from the order email.");
  const response = await reviewRequest("details");
  const order = await response.json();
  const summary = document.querySelector("#review-summary");
  summary.append(
    addDetail("Order", order.order_id.slice(0, 8).toUpperCase()),
    addDetail("Name", order.name),
    addDetail("Phone", order.phone),
    addDetail("Address", order.address),
    addDetail("Payment reference", order.payment_reference),
    addDetail("Items", order.items.map((item) => `${item.name} × ${item.quantity}`).join(", ")),
    addDetail("Total", `₹${order.total}`),
    addDetail("Customer note", order.note),
  );
  if (order.has_proof) {
    const imageResponse = await reviewRequest("proof");
    const image = document.querySelector("#proof-preview");
    image.src = URL.createObjectURL(await imageResponse.blob());
    document.querySelector("#proof-section").hidden = false;
  }
  detailsPanel.hidden = false;
  statusMessage.hidden = true;
}

async function decide(action) {
  const reason = document.querySelector("#rejection-reason").value.trim();
  if (action === "reject" && reason.length < 4) {
    statusMessage.hidden = false;
    statusMessage.textContent = "Please enter a clear rejection reason (at least 4 characters).";
    document.querySelector("#rejection-reason").focus();
    return;
  }
  const buttons = document.querySelectorAll(".review-actions button");
  buttons.forEach((button) => { button.disabled = true; });
  statusMessage.hidden = false;
  statusMessage.textContent = action === "approve" ? "Saving approval…" : "Saving rejection…";
  try {
    await reviewRequest(action, reason);
    detailsPanel.hidden = true;
    statusMessage.textContent = action === "approve"
      ? "Order accepted. The customer will see the confirmation and invoice option."
      : "Order rejected. The customer will see your reason on the order status page.";
  } catch (error) {
    statusMessage.textContent = error.message;
    buttons.forEach((button) => { button.disabled = false; });
  }
}

document.querySelector("#approve-order").addEventListener("click", () => decide("approve"));
document.querySelector("#reject-order").addEventListener("click", () => decide("reject"));
loadReview().catch((error) => {
  statusMessage.textContent = error.message || "Could not load this review.";
});
