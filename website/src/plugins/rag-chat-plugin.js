/**
 * Docusaurus RAG Chat Plugin
 *
 * Adds a /chat route to the Docusaurus site that displays the RAG chatbot.
 * This plugin:
 * - Creates a dedicated /chat page
 * - Loads the RagChat component
 * - Integrates with Docusaurus routing
 */

module.exports = function ragChatPlugin(context, options) {
  return {
    name: "rag-chat-plugin",

    // Extend the Docusaurus routes
    getRoutes() {
      return [
        {
          path: "/chat",
          component: "@site/src/pages/Chat.tsx",
          exact: true,
        },
      ];
    },

    // Extend client config
    extendCli(cli) {
      cli.command("rag:ingest")
        .description("Run RAG document ingestion")
        .action(async () => {
          // This would trigger the ingest script if needed
          console.log(
            "RAG ingestion should be run separately: python scripts/ingest_documents.py"
          );
        });
    },
  };
};
