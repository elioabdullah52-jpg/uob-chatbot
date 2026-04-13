const {
  getTrimmedQuestion,
  getSenderLabel,
  buildMetaText,
  shouldSendOnKeydown
} = require("./chat_utils");

test("getTrimmedQuestion returns trimmed text", () => {
  expect(getTrimmedQuestion("  hello  ")).toBe("hello");
});

test("getTrimmedQuestion returns empty string for blank input", () => {
  expect(getTrimmedQuestion("   ")).toBe("");
});

test("getSenderLabel returns You for user", () => {
  expect(getSenderLabel("user")).toBe("You");
});

test("getSenderLabel returns Bot for bot", () => {
  expect(getSenderLabel("bot")).toBe("Bot");
});

test("buildMetaText builds correct label", () => {
  expect(buildMetaText("user", "10:15")).toBe("You • 10:15");
});

test("shouldSendOnKeydown returns true for Enter without Shift", () => {
  expect(shouldSendOnKeydown("Enter", false)).toBe(true);
});

test("shouldSendOnKeydown returns false for Shift+Enter", () => {
  expect(shouldSendOnKeydown("Enter", true)).toBe(false);
});

test("shouldSendOnKeydown returns false for other keys", () => {
  expect(shouldSendOnKeydown("a", false)).toBe(false);
});
