function getTrimmedQuestion(value) {
  return String(value || "").trim();
}

function getSenderLabel(who) {
  return who === "user" ? "You" : "Bot";
}

function buildMetaText(who, timeText) {
  return `${getSenderLabel(who)} • ${timeText}`;
}

function shouldSendOnKeydown(key, shiftKey) {
  return key === "Enter" && !shiftKey;
}

if (typeof module !== "undefined") {
  module.exports = {
    getTrimmedQuestion,
    getSenderLabel,
    buildMetaText,
    shouldSendOnKeydown
  };
}
