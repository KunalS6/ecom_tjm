const orderPage = document.querySelector("#customer-order");
const publicId = orderPage.dataset.orderId;
const language = document.documentElement.lang;
const orderToken = window.location.hash.slice(1);
const statusElement = document.querySelector("#customer-order-status");
const receiptButton = document.querySelector("#download-receipt");
const messages = language === "bn"
  ? {
    invalid: "অর্ডারের লিংকটি সঠিক নয়। অর্ডারের বার্তা থেকে লিংকটি খুলুন।",
    confirmed: `আপনার অর্ডার ${publicId.slice(0, 8).toUpperCase()} গ্রহণ করা হয়েছে।`,
    rejected: `অর্ডার ${publicId.slice(0, 8).toUpperCase()} গ্রহণ করা যায়নি।`,
    waiting: `অর্ডার ${publicId.slice(0, 8).toUpperCase()} ব্যবসার পর্যালোচনার অপেক্ষায় আছে।`,
    rejectionReason: "বাতিলের কারণ",
    name: "নাম",
    phone: "ফোন",
    address: "ঠিকানা",
    items: "পণ্য",
    total: "মোট",
    paymentReference: "পেমেন্ট রেফারেন্স",
    note: "বিশেষ নির্দেশ",
    statusError: "অর্ডারের অবস্থা দেখা যায়নি।",
    pdfError: "PDF ডাউনলোড করা যায়নি।",
  }
  : {
    invalid: "This order link is invalid. Please open the link from your order message.",
    confirmed: `Your order ${publicId.slice(0, 8).toUpperCase()} has been accepted.`,
    rejected: `Order ${publicId.slice(0, 8).toUpperCase()} could not be accepted.`,
    waiting: `Order ${publicId.slice(0, 8).toUpperCase()} is waiting for the business to review it.`,
    rejectionReason: "Reason for rejection",
    name: "Name",
    phone: "Phone",
    address: "Address",
    items: "Items",
    total: "Total",
    paymentReference: "Payment reference",
    note: "Special instructions",
    statusError: "Could not check the order.",
    pdfError: "The PDF could not be downloaded.",
  };

history.replaceState(null, "", window.location.pathname);

async function getStatus() {
  const response = await fetch(`/api/orders/${publicId}/status`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ token: orderToken }),
  });
  const result = await response.json();
  if (!response.ok) throw new Error(result.error || messages.statusError);
  return result;
}

async function downloadReceipt() {
  const response = await fetch(`/api/orders/${publicId}/receipt.pdf`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ token: orderToken }),
  });
  if (!response.ok) throw new Error(messages.pdfError);
  const url = URL.createObjectURL(await response.blob());
  const link = document.createElement("a");
  link.href = url;
  link.download = `tok-jhal-order-${publicId.slice(0, 8)}.pdf`;
  link.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

function renderOrderDetails(order) {
  const container = document.querySelector("#customer-order-details");
  const rows = [
    [messages.name, order.name],
    [messages.phone, order.phone],
    [messages.address, order.address],
    [messages.items, order.items.map((item) => `${item.name} × ${item.quantity}`).join(", ")],
    [messages.total, new Intl.NumberFormat(language === "bn" ? "bn-IN" : "en-IN", {
      style: "currency",
      currency: "INR",
      maximumFractionDigits: 0,
    }).format(order.total)],
    ...(order.payment_reference ? [[messages.paymentReference, order.payment_reference]] : []),
    ...(order.note ? [[messages.note, order.note]] : []),
  ];
  container.replaceChildren(...rows.map(([label, value]) => {
    const row = document.createElement("p");
    const heading = document.createElement("strong");
    heading.textContent = `${label}: `;
    row.append(heading, document.createTextNode(value));
    return row;
  }));
  container.hidden = false;
}

async function pollStatus() {
  if (!orderToken) {
    statusElement.textContent = messages.invalid;
    return;
  }
  try {
    const order = await getStatus();
    if (order.status === "approved") {
      statusElement.textContent = messages.confirmed;
      renderOrderDetails(order);
      receiptButton.hidden = false;
      return;
    }
    if (order.status === "payment_rejected") {
      statusElement.textContent = messages.rejected;
      renderOrderDetails(order);
      const rejection = document.querySelector("#customer-rejection-reason");
      rejection.textContent = `${messages.rejectionReason}: ${order.rejection_reason}`;
      rejection.hidden = false;
      return;
    }
    statusElement.textContent = messages.waiting;
    window.setTimeout(pollStatus, 7000);
  } catch (error) {
    statusElement.textContent = error.message;
  }
}

receiptButton.addEventListener("click", () => {
  downloadReceipt().catch((error) => { statusElement.textContent = error.message; });
});
pollStatus();
