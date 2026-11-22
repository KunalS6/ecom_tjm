const toBengaliDigits = (value) => String(value).replace(/\d/g, (digit) => "০১২৩৪৫৬৭৮৯"[digit]);
const translations = {
  bn: {
    metaDescription: "টক ঝাল মিষ্টি কো.-র ঘরোয়া আচার, নাড়ু আর পাপড়—বাঙালির চেনা স্বাদ, যত্নে তৈরি।",
    brandHome: "টক ঝাল মিষ্টি কো. — হোম",
    logoAlt: "টক ঝাল মিষ্টি কো. — প্রতিটি খাবারে স্বাদের ছোঁয়া",
    announcement: "প্রতিটি স্বাদে মিশে আছে ঘরের যত্ন",
    navLabel: "মূল নেভিগেশন",
    navProducts: "সব পণ্য",
    navPickles: "আচার",
    navHomemade: "ঘরোয়া পণ্য",
    navStory: "আমাদের কথা",
    bag: "ব্যাগ",
    openBag: "শপিং ব্যাগ খুলুন",
    closeBag: "ব্যাগ বন্ধ করুন",
    closeForm: "ফর্ম বন্ধ করুন",
    heroImage: "আচার ও ঘরোয়া খাবারের সাজানো থালা",
    jarMango: "আমের<br>আচার",
    jarLemon: "লেবুর<br>আচার",
    artCaption: "হাতে বানানো, মন থেকে",
    heroEyebrow: "একটু ঘর, একটু ভালোবাসা",
    heroTitle: "বাঙালির চেনা স্বাদ,<br><em>ঘরের যত্নে</em> তৈরি",
    heroDescription: "আচারের টক-ঝাল থেকে নাড়ুর মিষ্টি—প্রতিটি কামড়ে ফিরে পান নিজের ঘরের সেই চেনা অনুভূতি।",
    heroCta: "স্বাদ বেছে নিন",
    heroStory: "আমাদের গল্প",
    heroNoteTitle: "যত্ন করে তৈরি",
    heroNoteText: "আপনার পরিবারের জন্য",
    heroBottom: "রসনায় বাঙালিয়ানা",
    promisesLabel: "আমাদের অঙ্গীকার",
    promiseHomeTitle: "ঘরোয়া ভালোবাসা",
    promiseHomeText: "প্রতিটি পণ্যে যত্নের ছোঁয়া",
    promiseTasteTitle: "চেনা বাঙালি স্বাদ",
    promiseTasteText: "যে স্বাদ মনে থেকে যায়",
    promiseCareTitle: "আপনার জন্যই তৈরি",
    promiseCareText: "ঘরের মানুষের কথা ভেবে",
    productsEyebrow: "ভালোবাসার সম্ভার",
    productsTitle: "কী খেতে ইচ্ছে করছে?",
    productsIntro: "চেনা স্বাদের ভাঁড়ার থেকে বেছে নিন আপনার পছন্দ।",
    searchPlaceholder: "পণ্য খুঁজুন...",
    searchLabel: "পণ্য খুঁজুন",
    filterLabel: "পণ্য বাছাই",
    filterAll: "সব পণ্য",
    filterPickle: "আচার",
    filterHomemade: "ঘরোয়া পণ্য",
    catalogNote: "ভালোবাসা দিয়ে বানানো",
    priceNote: "দামগুলো নমুনা হিসেবে দেখানো হয়েছে—ব্যবসার প্রকৃত দাম, প্যাকেটের পরিমাণ ও ডেলিভারি চার্জ বসিয়ে নিন।",
    loading: "আপনার পছন্দের স্বাদগুলো আসছে…",
    productsError: "পণ্যগুলো এখন দেখা যাচ্ছে না। একটু পরে আবার চেষ্টা করুন।",
    emptySearch: "এই নামে কোনো পণ্য পাওয়া যায়নি। অন্য কিছু লিখে দেখুন।",
    productCategoryPickle: "ঘরোয়া আচার",
    productCategoryHomemade: "ঘরে তৈরি",
    perItem: "প্রতি পিস",
    addProduct: "{name} ব্যাগে যোগ করুন",
    storyStampTop: "ঘরের",
    storyStampMain: "স্বাদ",
    storyStampBottom: "ঘরের",
    storyCaption: "ভালোবাসায় মাখা বাঙালিয়ানা",
    storyEyebrow: "আমাদের ছোট্ট গল্প",
    storyTitle: "একটু টক, একটু ঝাল,<br><em>আর অনেকটা ভালোবাসা।</em>",
    storyP1: "কিছু স্বাদ শুধু জিভে লাগে না—মনে গেঁথে থাকে। সেই চেনা ঘরোয়া স্বাদ আর আপন মানুষের যত্নকে সঙ্গে নিয়েই আমাদের পথচলা।",
    storyP2: "আচারের বয়াম হোক কিংবা নাড়ুর মিষ্টি—প্রতিটি পণ্যে থাকুক নিজের বাড়ির মতো আপন অনুভূতি।",
    storyLink: "আমাদের স্বাদগুলো দেখুন",
    bannerEyebrow: "প্রিয়জনের সঙ্গে ভাগ করে নিন",
    bannerTitle: "ঘরের স্বাদ ছড়িয়ে পড়ুক<br>আপন মানুষের কাছে।",
    bannerCta: "পছন্দের পণ্য বেছে নিন",
    footerNote: "বাঙালির চেনা স্বাদে, ঘরের ভালোবাসায়।",
    cartKicker: "আপনার পছন্দ",
    cartTitle: "শপিং ব্যাগ",
    subtotal: "সাবটোটাল",
    deliveryNote: "ডেলিভারি চার্জ অর্ডার নিশ্চিত করার সময় জানানো হবে।",
    checkout: "অর্ডার এগিয়ে নিন",
    checkoutKicker: "আর এক ধাপ",
    checkoutTitle: "ডেলিভারির তথ্য",
    checkoutIntro: "অর্ডারের অবস্থা ইমেলে জানাতে আপনার ইমেল ঠিকানা দিন।",
    nameLabel: "আপনার নাম",
    namePlaceholder: "যে নামে অর্ডার করবেন",
    phoneLabel: "ফোন নম্বর",
    phonePlaceholder: "আপনার যোগাযোগের নম্বর",
    emailLabel: "ইমেল ঠিকানা",
    emailPlaceholder: "অর্ডারের আপডেট পাওয়ার ইমেল",
    addressLabel: "সম্পূর্ণ ঠিকানা",
    addressPlaceholder: "বাড়ি, রাস্তা, এলাকা ও পিন/পোস্টকোড",
    noteLabel: "বিশেষ নির্দেশ",
    optional: "(ঐচ্ছিক)",
    notePlaceholder: "ডেলিভারি সংক্রান্ত কোনো কথা থাকলে লিখুন",
    orderTotal: "মোট পণ্যমূল্য",
    confirmOrder: "অর্ডার নিশ্চিত করুন",
    paymentNote: "অর্ডার পাঠানোর পর ইমেলে পর্যালোচনার লিংক যাবে। সিদ্ধান্ত হলে এই পাতায় কারণ/নিশ্চিতকরণ দেখা যাবে।",
    checkoutNoticeTitle: "অর্ডারের তথ্য নিরাপদে সংরক্ষণ করা হবে",
    checkoutNoticeText: "পেমেন্টের নম্বর এখনো যোগ করা হয়নি। ব্যবসার পক্ষ থেকে পেমেন্টের নির্দেশনা না পাওয়া পর্যন্ত টাকা পাঠাবেন না।",
    paymentReferenceLabel: "পেমেন্টের রেফারেন্স নম্বর",
    paymentReferencePlaceholder: "UPI লেনদেনের রেফারেন্স নম্বর",
    paymentProofLabel: "পেমেন্টের স্ক্রিনশট",
    paymentProofHelp: "JPG, PNG বা WebP · সর্বোচ্চ ৫ MB",
    noFileChosen: "কোনো ফাইল বেছে নেওয়া হয়নি",
    proofConsent: "স্ক্রিনশট দিলে সেটি নিরাপদে পর্যালোচনার জন্য সম্মতি দিচ্ছি।",
    paymentProofError: "সঠিক JPG, PNG অথবা WebP স্ক্রিনশট দিন (সর্বোচ্চ ৫ MB)।",
    consentError: "স্ক্রিনশট পর্যালোচনার সম্মতিতে টিক দিন।",
    orderResultKicker: "অর্ডারের অবস্থা",
    orderPendingTitle: "আপনার অর্ডার পর্যালোচনায় আছে",
    orderPendingCopy: "আপনার অর্ডার সংরক্ষণ করা হয়েছে। ইমেলে পাঠানো লিংক থেকে ব্যবসা অর্ডারটি পর্যালোচনা করবে।",
    orderReferenceLabel: "অর্ডার নম্বর",
    orderNotificationFailed: "অর্ডারটি সংরক্ষিত, কিন্তু ইমেল পাঠানো যায়নি। আবার অর্ডার করবেন না—দয়া করে দোকানের সঙ্গে যোগাযোগ করুন।",
    orderNotificationTest: "ইমেল সেটআপ করা নেই। রিভিউ লিংক সার্ভারের টার্মিনালে আছে।",
    orderApprovedTitle: "আপনার অর্ডার নিশ্চিত!",
    orderApprovedCopy: "আপনার অর্ডার গৃহীত হয়েছে। নিচে অর্ডারের বিবরণ দেখুন এবং ইনভয়েস ডাউনলোড করুন।",
    orderRejectedTitle: "অর্ডারটি গ্রহণ করা যায়নি",
    orderRejectedCopy: "ব্যবসার দেওয়া কারণটি নিচে দেখুন।",
    rejectionReasonLabel: "বাতিলের কারণ",
    orderCustomerLabel: "নাম",
    orderPhoneLabel: "ফোন",
    orderAddressLabel: "ঠিকানা",
    orderItemsLabel: "পণ্য",
    orderTotalLabel: "মোট",
    orderPaymentReferenceLabel: "পেমেন্ট রেফারেন্স",
    orderNoteLabel: "বিশেষ নির্দেশ",
    openOrderStatus: "অর্ডারের অবস্থা দেখুন",
    downloadReceipt: "অর্ডার নিশ্চিতকরণ PDF ডাউনলোড",
    pdfDownloadError: "PDF ডাউনলোড করা যায়নি। আবার চেষ্টা করুন।",
    cartEmpty: "আপনার ব্যাগ এখনো খালি",
    cartEmptyHint: "পছন্দের স্বাদগুলো যোগ করে নিন।",
    decreaseQuantity: "{name} একটি কমান",
    increaseQuantity: "{name} একটি বাড়ান",
    maxQuantity: "একটি পণ্যের সর্বোচ্চ ২০টি যোগ করা যাবে।",
    addToast: "{name} ব্যাগে যোগ হয়েছে।",
    submitting: "অর্ডার পাঠানো হচ্ছে…",
    orderSuccess: "অর্ডার #{id} পেয়েছি। ধন্যবাদ!",
    orderError: "অর্ডার পাঠানো যায়নি। আবার চেষ্টা করুন।",
    contactError: "যোগাযোগে সমস্যা হয়েছে। আবার চেষ্টা করুন।",
    nameError: "নাম ২ থেকে ৮০ অক্ষরের মধ্যে লিখুন।",
    phoneError: "সঠিক ফোন নম্বর লিখুন (৭–১৫টি সংখ্যা)।",
    emailError: "সঠিক ইমেল ঠিকানা লিখুন।",
    addressError: "সম্পূর্ণ ঠিকানা লিখুন (কমপক্ষে ৮ অক্ষর)।",
    noteError: "নোট ৫০০ অক্ষরের মধ্যে লিখুন।",
    emptyOrderError: "অর্ডারে অন্তত একটি পণ্য যোগ করুন।",
    badItemsError: "পণ্যের তালিকা সঠিক নয়।",
    orderLimitError: "একটি পণ্যের সর্বোচ্চ ২০টি অর্ডার করা যাবে।",
    genericFormError: "তথ্যগুলো একবার দেখে নিন।",
  },
  en: {
    metaDescription: "Tok Jhal Misti Co. — homemade Bengali pickles, sweets, and papad, made with love.",
    brandHome: "Tok Jhal Misti Co. — home",
    logoAlt: "Tok Jhal Misti Co. — Bringing flavours to every meal",
    announcement: "A little taste of home in every bite",
    navLabel: "Main navigation",
    navProducts: "Shop all",
    navPickles: "Pickles",
    navHomemade: "Homemade treats",
    navStory: "Our story",
    bag: "Bag",
    openBag: "Open shopping bag",
    closeBag: "Close shopping bag",
    closeForm: "Close form",
    heroImage: "An artful spread of pickles and homemade treats",
    jarMango: "Mango<br>pickle",
    jarLemon: "Lemon<br>pickle",
    artCaption: "Handmade, from the heart",
    heroEyebrow: "A little home, a lot of love",
    heroTitle: "The Bengali flavours<br>you know, <em>made with care</em>",
    heroDescription: "From tangy, spicy pickles to sweet naru—bring home the comforting flavours that feel like family.",
    heroCta: "Find your flavour",
    heroStory: "Our story",
    heroNoteTitle: "Made with care",
    heroNoteText: "For your family",
    heroBottom: "A taste of Bengal",
    promisesLabel: "Our promises",
    promiseHomeTitle: "Made with homegrown love",
    promiseHomeText: "A little care in every batch",
    promiseTasteTitle: "True Bengali flavours",
    promiseTasteText: "The tastes that stay with you",
    promiseCareTitle: "Thoughtfully homemade",
    promiseCareText: "Made with your family in mind",
    productsEyebrow: "A little something to love",
    productsTitle: "What are you craving?",
    productsIntro: "Find a familiar favourite in our little pantry.",
    searchPlaceholder: "Search the shop...",
    searchLabel: "Search products",
    filterLabel: "Filter products",
    filterAll: "All products",
    filterPickle: "Pickles",
    filterHomemade: "Homemade",
    catalogNote: "Lovingly homemade",
    priceNote: "Prices shown are examples. Please confirm actual prices, pack sizes, and delivery charges before placing an order.",
    loading: "Bringing your favourite flavours...",
    productsError: "Products are unavailable right now. Please try again in a moment.",
    emptySearch: "No products found. Try another search.",
    productCategoryPickle: "Homemade pickle",
    productCategoryHomemade: "Homemade treat",
    perItem: "per item",
    addProduct: "Add {name} to bag",
    storyStampTop: "Made",
    storyStampMain: "with",
    storyStampBottom: "love",
    storyCaption: "A little Bengal in every bite",
    storyEyebrow: "A little about us",
    storyTitle: "A little tang, a little spice,<br><em>and a whole lot of love.</em>",
    storyP1: "Some flavours do more than delight your taste buds—they stay with you. We started with the comfort of familiar homemade recipes and the care of people who cook for family.",
    storyP2: "From a jar of pickle to a sweet naru, we hope every bite feels like a little piece of home.",
    storyLink: "Explore our flavours",
    bannerEyebrow: "Made for sharing with your favourite people",
    bannerTitle: "Share a taste of home<br>with someone you love.",
    bannerCta: "Find your favourites",
    footerNote: "Familiar Bengali flavours, made with a little love.",
    cartKicker: "Your picks",
    cartTitle: "Shopping bag",
    subtotal: "Subtotal",
    deliveryNote: "Delivery charges will be confirmed when we follow up on your order.",
    checkout: "Continue to checkout",
    checkoutKicker: "Almost there",
    checkoutTitle: "Delivery details",
    checkoutIntro: "Enter your email so we can send updates when the business reviews your order.",
    nameLabel: "Your name",
    namePlaceholder: "Name for the order",
    phoneLabel: "Phone number",
    phonePlaceholder: "Your contact number",
    emailLabel: "Email address",
    emailPlaceholder: "Where to send your order updates",
    addressLabel: "Full delivery address",
    addressPlaceholder: "House, street, area and PIN/postcode",
    noteLabel: "Special instructions",
    optional: "(optional)",
    notePlaceholder: "Anything we should know for delivery?",
    orderTotal: "Product total",
    confirmOrder: "Place your order",
    paymentNote: "After submission, the business gets a review link by email. This page will show the decision and its reason.",
    checkoutNoticeTitle: "Your order details will be saved securely",
    checkoutNoticeText: "A payment number has not been added yet. Do not send money until the business shares payment instructions.",
    paymentReferenceLabel: "Payment reference",
    paymentReferencePlaceholder: "UPI transaction ID / reference",
    paymentProofLabel: "Payment screenshot",
    paymentProofHelp: "JPG, PNG, or WebP · up to 5 MB",
    noFileChosen: "No file selected",
    proofConsent: "If I attach a screenshot, I agree to have it reviewed privately.",
    paymentProofError: "Choose a valid JPG, PNG, or WebP screenshot (up to 5 MB).",
    consentError: "Please confirm you understand how the screenshot will be reviewed.",
    orderResultKicker: "Order status",
    orderPendingTitle: "Your order is under review",
    orderPendingCopy: "Your order has been saved. The business will review it using the secure link sent by email.",
    orderReferenceLabel: "Order number",
    orderNotificationFailed: "Your order was saved, but the email could not be sent. Please contact the shop; do not submit the order again.",
    orderNotificationTest: "Email is not configured. The review link is in the server terminal.",
    orderApprovedTitle: "Your order is confirmed!",
    orderApprovedCopy: "Your order has been accepted. Review the details below and download your invoice.",
    orderRejectedTitle: "Your order could not be accepted",
    orderRejectedCopy: "See the reason provided by the business below.",
    rejectionReasonLabel: "Reason for rejection",
    orderCustomerLabel: "Name",
    orderPhoneLabel: "Phone",
    orderAddressLabel: "Address",
    orderItemsLabel: "Items",
    orderTotalLabel: "Total",
    orderPaymentReferenceLabel: "Payment reference",
    orderNoteLabel: "Special instructions",
    openOrderStatus: "View order status",
    downloadReceipt: "Download order confirmation PDF",
    pdfDownloadError: "The PDF could not be downloaded. Please try again.",
    cartEmpty: "Your bag is waiting for a treat",
    cartEmptyHint: "Add a few favourites to get started.",
    decreaseQuantity: "Remove one {name}",
    increaseQuantity: "Add one {name}",
    maxQuantity: "You can order up to 20 of each product.",
    addToast: "{name} added to your bag.",
    submitting: "Placing your order...",
    orderSuccess: "Order #{id} received. Thank you!",
    orderError: "We couldn't place your order. Please try again.",
    contactError: "We couldn't connect. Please try again.",
    nameError: "Please enter a name between 2 and 80 characters.",
    phoneError: "Please enter a valid phone number (7–15 digits).",
    emailError: "Please enter a valid email address.",
    addressError: "Please enter a complete address (at least 8 characters).",
    noteError: "Please keep your note under 500 characters.",
    emptyOrderError: "Please add at least one product to your order.",
    badItemsError: "The product list is invalid.",
    orderLimitError: "You can order up to 20 of each product.",
    genericFormError: "Please check your details and try again.",
  },
};
const englishProductDetails = {
  "aamer-achar": ["Mango pickle", "Tangy raw mango with familiar Bengali spices", "A Bengali favourite"],
  "lonkar-achar": ["Chilli pickle", "A lively chilli kick for your everyday meal", "For spice lovers"],
  "lebur-achar": ["Lemon pickle", "Bright sweet-and-sour lemon with homestyle spices", "Sweet & tangy"],
  "kooler-achar": ["Jujube pickle", "Seasonal jujube with a sweet, tangy bite", "Seasonal favourite"],
  "gurer-naru": ["Jaggery naru", "Coconut and the cosy sweetness of jaggery", "A homestyle favourite"],
  papad: ["Papad", "A crunchy companion for meals and teatime", "Crispy & light"],
  "chinir-naru": ["Sugar naru", "A little sweet bite with a hint of childhood", "A sweet little treat"],
  "sirir-naru": ["Siri naru", "A traditional homemade sweet to share", "Made with love"],
};
const productGrid = document.querySelector("#product-grid");
const cartCount = document.querySelector("#cart-count");
const cartOverlay = document.querySelector("#cart-overlay");
const checkoutModal = document.querySelector("#checkout-modal");
const orderModal = document.querySelector("#order-modal");
const cartItems = document.querySelector("#cart-items");
const form = document.querySelector("#checkout-form");
const toast = document.querySelector("#toast");
const productColors = ["#f1e4ce", "#efe1d9", "#f0e8c8", "#e5ebd7", "#eee1d1", "#e5e9d9", "#f2e3c9", "#e9e0ec"];

let products = [];
let cart = loadCart();
let activeFilter = "all";
let searchTerm = "";
let toastTimer;
let language = loadLanguage();
let activeOrder = null;
let statusPollTimer = null;

function loadLanguage() {
  try {
    return localStorage.getItem("tokjhal-language") === "en" ? "en" : "bn";
  } catch (error) {
    console.warn("Could not restore the preferred language.", error);
    return "bn";
  }
}

function text(key, values = {}) {
  return Object.entries(values).reduce(
    (result, [name, value]) => result.replaceAll(`{${name}}`, value),
    translations[language][key],
  );
}

function formatPrice(value) {
  return new Intl.NumberFormat(language === "bn" ? "bn-IN" : "en-IN", {
    style: "currency",
    currency: "INR",
    maximumFractionDigits: 0,
  }).format(value);
}

function setLanguage(nextLanguage) {
  language = nextLanguage;
  document.documentElement.lang = language;
  document.title = language === "bn"
    ? "টক ঝাল মিষ্টি কো. — ঘরের স্বাদ, মনভরা ভালোবাসা"
    : "Tok Jhal Misti Co. — A little taste of home";
  document.querySelector('meta[name="description"]').content = text("metaDescription");
  document.querySelectorAll("[data-i18n]").forEach((element) => {
    element.textContent = text(element.dataset.i18n);
  });
  document.querySelectorAll("[data-i18n-html]").forEach((element) => {
    element.innerHTML = text(element.dataset.i18nHtml);
  });
  document.querySelectorAll("[data-i18n-placeholder]").forEach((element) => {
    element.placeholder = text(element.dataset.i18nPlaceholder);
  });
  document.querySelectorAll("[data-i18n-aria]").forEach((element) => {
    element.setAttribute("aria-label", text(element.dataset.i18nAria));
  });
  document.querySelectorAll("[data-i18n-alt]").forEach((element) => {
    element.alt = text(element.dataset.i18nAlt);
  });
  document.querySelectorAll("[data-language]").forEach((button) => {
    const active = button.dataset.language === language;
    button.classList.toggle("active", active);
    button.setAttribute("aria-pressed", String(active));
  });
  document.querySelectorAll(".filter-tab span:first-child").forEach((element) => {
    const key = {
      all: "filterAll",
      pickle: "filterPickle",
      homemade: "filterHomemade",
    }[element.closest(".filter-tab").dataset.filter];
    element.textContent = text(key);
  });
  document.querySelectorAll(".filter-tab [data-count]").forEach((element) => {
    const count = Number(element.dataset.count);
    element.textContent = language === "bn" ? toBengaliDigits(count) : String(count).padStart(2, "0");
  });
  try {
    localStorage.setItem("tokjhal-language", language);
  } catch (error) {
    console.warn("Could not save the preferred language.", error);
  }
  renderProducts();
  renderCart();
  document.querySelector("#current-year").textContent = language === "bn"
    ? toBengaliDigits(new Date().getFullYear())
    : String(new Date().getFullYear());
}

function loadCart() {
  try {
    const saved = JSON.parse(localStorage.getItem("tokjhal-cart") || "{}");
    if (!saved || typeof saved !== "object" || Array.isArray(saved)) return {};
    return Object.fromEntries(
      Object.entries(saved).filter(([, quantity]) => Number.isInteger(quantity) && quantity > 0 && quantity <= 20),
    );
  } catch (error) {
    console.warn("Could not restore the saved shopping bag.", error);
    return {};
  }
}

function saveCart() {
  try {
    localStorage.setItem("tokjhal-cart", JSON.stringify(cart));
  } catch (error) {
    console.warn("Could not save the shopping bag in this browser.", error);
  }
}

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, (character) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;",
  })[character]);
}

async function loadProducts() {
  productGrid.innerHTML = `<div class="loading-state">${text("loading")}</div>`;
  try {
    const response = await fetch("/api/products");
    if (!response.ok) throw new Error(`Product list request failed (${response.status}).`);
    products = await response.json();
    renderProducts();
    renderCart();
  } catch (error) {
    console.error("Could not load products.", error);
    productGrid.innerHTML = `<p class="empty-search">${text("productsError")}</p>`;
  }
}

function renderProducts() {
  const visibleProducts = products.filter((product) => {
    const matchesCategory = activeFilter === "all" || product.category === activeFilter;
    const translated = englishProductDetails[product.id];
    const matchesSearch = `${product.name} ${product.english_name} ${product.description} ${translated?.join(" ") || ""}`
      .toLocaleLowerCase("bn")
      .includes(searchTerm);
    return matchesCategory && matchesSearch;
  });

  if (!visibleProducts.length) {
    productGrid.innerHTML = `<p class="empty-search">${text("emptySearch")}</p>`;
    return;
  }

  productGrid.innerHTML = visibleProducts.map((product) => {
    const index = products.indexOf(product) % productColors.length;
    const englishDetails = englishProductDetails[product.id];
    const name = language === "en" ? englishDetails[0] : product.name;
    const description = language === "en" ? englishDetails[1] : product.description;
    const label = language === "en" ? englishDetails[2] : product.label;
    const category = product.category === "pickle" ? text("productCategoryPickle") : text("productCategoryHomemade");
    return `
      <article class="product-card">
        <div class="product-visual" style="--visual-bg:${productColors[index]}">
          <span class="product-badge">${escapeHtml(label)}</span>
          <span class="product-icon" role="img" aria-label="${escapeHtml(name)}">${escapeHtml(product.icon)}</span>
        </div>
        <div class="product-info">
          <span class="product-category">${category}</span>
          <h3>${escapeHtml(name)}</h3>
          <p class="product-description">${escapeHtml(description)}</p>
          <div class="product-bottom">
            <span class="product-price">${formatPrice(product.price)} <small>${text("perItem")}</small></span>
            <button class="add-button" type="button" data-add="${escapeHtml(product.id)}" aria-label="${escapeHtml(text("addProduct", { name }))}">+</button>
          </div>
        </div>
      </article>`;
  }).join("");
}

function getTotal() {
  return products.reduce((sum, product) => sum + product.price * (cart[product.id] || 0), 0);
}

function renderCart() {
  const totalItems = Object.values(cart).reduce((sum, quantity) => sum + quantity, 0);
  cartCount.textContent = language === "bn" ? toBengaliDigits(totalItems) : String(totalItems);
  document.querySelector("#cart-total").textContent = formatPrice(getTotal());
  document.querySelector("#checkout-total").textContent = formatPrice(getTotal());
  document.querySelector("#checkout-button").disabled = totalItems === 0;

  const lines = products.filter((product) => cart[product.id]);
  if (!lines.length) {
    cartItems.innerHTML = `<div class="cart-empty"><span aria-hidden="true">🧺</span><strong>${text("cartEmpty")}</strong><p>${text("cartEmptyHint")}</p></div>`;
    return;
  }

  cartItems.innerHTML = lines.map((product) => {
    const name = language === "en" ? englishProductDetails[product.id][0] : product.name;
    const quantity = language === "bn" ? toBengaliDigits(cart[product.id]) : String(cart[product.id]);
    return `
      <article class="cart-line">
        <span class="cart-line-icon" aria-hidden="true">${escapeHtml(product.icon)}</span>
        <div class="cart-line-info">
          <strong>${escapeHtml(name)}</strong>
          <small>${formatPrice(product.price)} ${text("perItem")}</small>
          <div class="quantity-control">
            <button type="button" data-quantity="-1" data-id="${escapeHtml(product.id)}" aria-label="${escapeHtml(text("decreaseQuantity", { name }))}">−</button>
            <span>${quantity}</span>
            <button type="button" data-quantity="1" data-id="${escapeHtml(product.id)}" aria-label="${escapeHtml(text("increaseQuantity", { name }))}">+</button>
          </div>
        </div>
        <span class="cart-line-price">${formatPrice(product.price * cart[product.id])}</span>
      </article>`;
  }).join("");
}

function updateCart(productId, change) {
  const nextQuantity = (cart[productId] || 0) + change;
  if (nextQuantity > 20) {
    showToast(text("maxQuantity"));
    return;
  }
  if (nextQuantity > 0) cart[productId] = nextQuantity;
  else delete cart[productId];
  saveCart();
  renderCart();
}

function showToast(message) {
  toast.textContent = message;
  toast.classList.add("visible");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove("visible"), 2600);
}

function getOrderError(result) {
  const fieldKey = Object.keys(result.fields || {})[0];
  const errors = {
    name: "nameError",
    phone: "phoneError",
    email: "emailError",
    address: "addressError",
    note: "noteError",
    payment_proof: "paymentProofError",
    proof_consent: "consentError",
    items: "badItemsError",
  };
  if (fieldKey === "items" && result.fields.items.includes("অন্তত একটি")) {
    return text("emptyOrderError");
  }
  if (fieldKey === "items" && result.fields.items.includes("সর্বোচ্চ")) {
    return text("orderLimitError");
  }
  return fieldKey ? text(errors[fieldKey] || "genericFormError") : (language === "en" ? text("orderError") : result.error || text("orderError"));
}

function setDialog(dialog, open) {
  dialog.hidden = !open;
  document.body.classList.toggle("dialog-open", open || !cartOverlay.hidden || !checkoutModal.hidden || !orderModal.hidden);
  if (open) dialog.querySelector("button, input, textarea")?.focus();
}

document.querySelector("#product-search").addEventListener("input", (event) => {
  searchTerm = event.target.value.trim().toLocaleLowerCase("bn");
  renderProducts();
});

document.querySelectorAll(".filter-tab").forEach((button) => {
  button.addEventListener("click", () => {
    activeFilter = button.dataset.filter;
    document.querySelectorAll(".filter-tab").forEach((tab) => tab.classList.toggle("active", tab === button));
    renderProducts();
  });
});

document.querySelectorAll("[data-nav-filter]").forEach((link) => {
  link.addEventListener("click", () => {
    activeFilter = link.dataset.navFilter;
    document.querySelectorAll(".filter-tab").forEach((tab) => tab.classList.toggle("active", tab.dataset.filter === activeFilter));
    renderProducts();
  });
});

document.querySelectorAll("[data-language]").forEach((button) => {
  button.addEventListener("click", () => setLanguage(button.dataset.language));
});

productGrid.addEventListener("click", (event) => {
  const button = event.target.closest("[data-add]");
  if (!button) return;
  updateCart(button.dataset.add, 1);
  const product = products.find((item) => item.id === button.dataset.add);
  const name = language === "en" ? englishProductDetails[product.id][0] : product.name;
  showToast(text("addToast", { name }));
});

cartItems.addEventListener("click", (event) => {
  const button = event.target.closest("[data-quantity]");
  if (button) updateCart(button.dataset.id, Number(button.dataset.quantity));
});

document.querySelector("#open-cart").addEventListener("click", () => setDialog(cartOverlay, true));
document.querySelectorAll("[data-close-cart]").forEach((button) => button.addEventListener("click", () => setDialog(cartOverlay, false)));
cartOverlay.addEventListener("click", (event) => {
  if (event.target === cartOverlay) setDialog(cartOverlay, false);
});

document.querySelector("#checkout-button").addEventListener("click", () => {
  if (Object.keys(cart).length) {
    setDialog(cartOverlay, false);
    setDialog(checkoutModal, true);
  }
});
document.querySelectorAll("[data-close-checkout]").forEach((button) => button.addEventListener("click", () => setDialog(checkoutModal, false)));
checkoutModal.addEventListener("click", (event) => {
  if (event.target === checkoutModal) setDialog(checkoutModal, false);
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") {
    setDialog(checkoutModal, false);
    setDialog(cartOverlay, false);
    setDialog(orderModal, false);
  }
});

document.querySelector("#close-order-modal").addEventListener("click", () => setDialog(orderModal, false));
orderModal.addEventListener("click", (event) => {
  if (event.target === orderModal) setDialog(orderModal, false);
});

document.querySelector("#payment-proof").addEventListener("change", (event) => {
  const file = event.target.files[0];
  const fileName = document.querySelector("#proof-file-name");
  const preview = document.querySelector("#proof-preview");
  const consentLabel = document.querySelector("#proof-consent-label");
  if (preview.dataset.objectUrl) URL.revokeObjectURL(preview.dataset.objectUrl);
  if (!file) {
    fileName.textContent = text("noFileChosen");
    preview.hidden = true;
    consentLabel.hidden = true;
    return;
  }
  fileName.textContent = file.name;
  consentLabel.hidden = false;
  const objectUrl = URL.createObjectURL(file);
  preview.src = objectUrl;
  preview.dataset.objectUrl = objectUrl;
  preview.hidden = false;
});

async function downloadReceipt() {
  if (!activeOrder) return;
  const response = await fetch(`/api/orders/${activeOrder.orderId}/receipt.pdf`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ token: activeOrder.receiptToken }),
  });
  if (!response.ok) throw new Error(text("pdfDownloadError"));
  const url = URL.createObjectURL(await response.blob());
  const link = document.createElement("a");
  link.href = url;
  link.download = `tok-jhal-order-${activeOrder.orderId.slice(0, 8)}.pdf`;
  link.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

function showOrderStatus(order) {
  activeOrder = order;
  document.querySelector("#order-reference").textContent = order.orderId.slice(0, 8).toUpperCase();
  document.querySelector("#open-order-status").href = `/order/${order.orderId}?lang=${language}#${order.receiptToken}`;
  document.querySelector("#order-result-title").textContent = text("orderPendingTitle");
  document.querySelector("#order-result-copy").textContent = text("orderPendingCopy");
  document.querySelector("#order-details").hidden = true;
  document.querySelector("#order-rejection-reason").hidden = true;
  document.querySelector("#order-notification-note").textContent = order.notificationStatus === "failed"
    ? text("orderNotificationFailed")
    : order.notificationStatus === "console"
      ? text("orderNotificationTest")
      : "";
  document.querySelector("#download-receipt").hidden = true;
  setDialog(orderModal, true);
  window.clearTimeout(statusPollTimer);
  pollOrderStatus();
}

async function pollOrderStatus() {
  if (!activeOrder) return;
  try {
    const response = await fetch(`/api/orders/${activeOrder.orderId}/status`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ token: activeOrder.receiptToken }),
    });
    if (!response.ok) throw new Error(`Order status request failed (${response.status}).`);
    const order = await response.json();
    if (order.status === "approved") {
      document.querySelector("#order-result-title").textContent = text("orderApprovedTitle");
      document.querySelector("#order-result-copy").textContent = text("orderApprovedCopy");
      renderOrderDetails(order);
      document.querySelector("#download-receipt").hidden = false;
      return;
    }
    if (order.status === "payment_rejected") {
      document.querySelector("#order-result-title").textContent = text("orderRejectedTitle");
      document.querySelector("#order-result-copy").textContent = text("orderRejectedCopy");
      renderOrderDetails(order);
      const reason = document.querySelector("#order-rejection-reason");
      reason.textContent = `${text("rejectionReasonLabel")}: ${order.rejection_reason}`;
      reason.hidden = false;
      return;
    }
  } catch (error) {
    console.error("Could not refresh order status.", error);
  }
  statusPollTimer = window.setTimeout(pollOrderStatus, 7000);
}

function renderOrderDetails(order) {
  const container = document.querySelector("#order-details");
  const rows = [
    [text("orderCustomerLabel"), order.name],
    [text("orderPhoneLabel"), order.phone],
    [text("orderAddressLabel"), order.address],
    [text("orderItemsLabel"), order.items.map((item) => `${item.name} × ${item.quantity}`).join(", ")],
    [text("orderTotalLabel"), formatPrice(order.total)],
    ...(order.payment_reference ? [[text("orderPaymentReferenceLabel"), order.payment_reference]] : []),
    ...(order.note ? [[text("orderNoteLabel"), order.note]] : []),
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

document.querySelector("#download-receipt").addEventListener("click", () => {
  downloadReceipt().catch((error) => showToast(error.message || text("pdfDownloadError")));
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const errorMessage = document.querySelector("#form-error");
  const submitButton = form.querySelector('[type="submit"]');
  errorMessage.textContent = "";
  const proofInput = document.querySelector("#payment-proof");
  const hasProof = proofInput.files.length > 0;
  if (hasProof && !form.elements.proof_consent.checked) {
    errorMessage.textContent = text("consentError");
    form.elements.proof_consent.focus();
    return;
  }
  submitButton.disabled = true;
  submitButton.textContent = text("submitting");

  const values = new FormData(form);
  const order = {
    name: values.get("name").trim(),
    phone: values.get("phone").trim(),
    email: values.get("email").trim(),
    address: values.get("address").trim(),
    note: values.get("note").trim(),
    payment_reference: values.get("payment_reference").trim(),
    proof_consent: values.get("proof_consent") === "on",
    language,
    items: Object.entries(cart).map(([id, quantity]) => ({ id, quantity })),
  };
  const submission = new FormData();
  submission.set("order", JSON.stringify(order));
  if (hasProof) submission.set("payment_proof", proofInput.files[0]);

  try {
    const response = await fetch("/api/orders", {
      method: "POST",
      body: submission,
    });
    const result = await response.json();
    if (!response.ok) {
      throw new Error(getOrderError(result));
    }

    cart = {};
    saveCart();
    form.reset();
    renderCart();
    document.querySelector("#proof-preview").hidden = true;
    document.querySelector("#proof-consent-label").hidden = true;
    document.querySelector("#proof-file-name").textContent = text("noFileChosen");
    setDialog(checkoutModal, false);
    showOrderStatus({
      orderId: result.order_id,
      receiptToken: result.receipt_token,
      notificationStatus: result.notification_status,
    });
  } catch (error) {
    console.error("Could not place the order.", error);
    errorMessage.textContent = error.message || text("contactError");
  } finally {
    submitButton.disabled = false;
    submitButton.innerHTML = `<span data-i18n="confirmOrder">${text("confirmOrder")}</span> <span aria-hidden="true">→</span>`;
  }
});

setLanguage(language);
loadProducts();