# Frontend Architecture

## UI Structure

The UI consists of a **Left Sidebar** and a **Right Main Panel**.

### 1. Left Sidebar
- Displays a list of all existing projects.
- Features a **"Create New Project"** button.
- Clicking a project selects it and loads its corresponding data into the Right Main Panel.

### 2. Right Main Panel
- The workspace for the currently selected project.
- Features a horizontal navigation bar with tabs mapped directly 1:1 to underlying database tables.
- The tabs are displayed in the following strict order:
  1. **Project Tab:** Displays the project title, description, tags, and all project-level fields. The UI consists of vertically stacked, editable text boxes to manually modify this data. Maps to the `projects` table.
  2. **Chat Tab:** For interacting with the AI agent. Used for brainstorming and issuing commands. Maps to the `messages` table.
  3. **Script Tab:** Contains the generated video scripts in vertically stacked editable text areas. Maps to the `scripts` table.
  4. **Social Network Tab:** Displays auto-generated captions, descriptions, and hashtags in vertically stacked editable text areas. Maps to the `social_media_posts` table.

## Workflow Execution

1. **Project Creation:**
   - User clicks "Create New Project".
   - Frontend calls the backend router.
   - Backend provisions a new project ID.
2. **Interaction (Brainstorming):**
   - User types in the **Chat Tab**.
   - Frontend sends the message to the `agent` router.
   - AI agent responds with brainstorming output. The backend saves the history to the `messages` table.
3. **Execution (Content Generation):**
   - User asks the agent to draft a script or a caption.
   - AI agent changes intent to execution mode and uses explicit function calling mapped to specific tables (e.g., `write_script`, `write_social_media`).
   - The backend directly saves the generated content to the specific destination table (`scripts` or `social_media_posts`).
   - Frontend detects the update and populates the corresponding tab.