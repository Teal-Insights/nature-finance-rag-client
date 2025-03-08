import {
  ChatMessage,
  ContentPosition,
  getSourceAnnotationData,
  useChatMessage,
  useChatUI,
} from "@llamaindex/chat-ui";
import { DeepResearchCard } from "./custom/deep-research-card";
import { Markdown } from "./custom/markdown";

export function ChatMessageContent() {
  const { isLoading, append } = useChatUI();
  const { message } = useChatMessage();
  const customContent = [
    {
      // override the default markdown component
      position: ContentPosition.MARKDOWN,
      component: (
        <Markdown
          content={message.content}
          sources={getSourceAnnotationData(message.annotations)?.[0]}
        />
      ),
    },
    // add the deep research card
    {
      position: ContentPosition.CHAT_EVENTS,
      component: <DeepResearchCard message={message} />,
    }
  ];
  return (
    <ChatMessage.Content
      content={customContent}
      isLoading={isLoading}
      append={append}
    />
  );
}
