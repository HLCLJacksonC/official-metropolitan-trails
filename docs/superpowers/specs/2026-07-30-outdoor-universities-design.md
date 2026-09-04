# Outdoor Universities Platform Design

**Date:** 2026-07-30

**Status:** Approved for specification

**Initial setting:** Small Shanghai pilot with fewer than ten invited participants

## 1. Product Thesis

Outdoor Universities is an open platform where people share stories, learning reflections, questions, observations, and source material. It recognizes the world outside formal institutions as a place of mutual learning: participants may become learners, storytellers, investigators, teachers, or collaborators at different moments.

The platform may support a generative pattern:

> story or material → question → shared offline inquiry → further stories or material

This is an opportunity, not a required workflow. A person may contribute once without joining a project or participating in an offline activity.

Outdoor Universities begins as a small Shanghai experiment but is not conceptually limited to Shanghai. Metropolitan Trails is the founder's current project and will be the platform's first substantial example; it does not define the platform's full subject matter.

## 2. Audience and Initial Scope

The first participants are fewer than ten friends, classmates, and collaborators. Artists, researchers, designers, and journalists may gradually join, but the initial product is not designed as a public social network. All pilot content is visible only to authenticated invited participants, not to the public web.

The first release is an invitation-based web application. It should establish a usable framework for real contributions without prematurely implementing governance, growth, recommendation, or institutional features.

### In scope

- Invite-based access and simple personal profiles
- Immediate publishing of lightweight contributions
- Contribution detail and knowledge responses
- Explicit relationships between contributions
- Persistent project spaces
- Adding existing contributions to projects
- Basic project participation
- Simple offline activity information inside projects
- Optional topics, places, and external links
- A populated Metropolitan Trails example project
- Mobile-first publishing and comfortable desktop reading

### Out of scope

- Public-platform moderation, reporting, appeals, and institutional permissions
- Algorithmic recommendations, popularity rankings, and follower metrics
- Direct messages and group chat
- Event registration and attendance management
- Course catalogs, certificates, credits, or fixed teacher-student roles
- A platform-owned GIS or complex map system
- Structured research-task management
- Multi-city portals and full multilingual infrastructure
- Growth, retention, or user-activity targets

## 3. Design Direction: Open Field

The visual and interaction direction is **Open Field**: an open learning site rather than a social feed, school portal, or specialist research database.

“Field” refers both to the outdoors and to a person's area of exploration. The interface may draw from field notes, public notices, workshop print matter, contact sheets, sound traces, specimens, route sketches, and digital works. These references should feel contemporary and usable, not nostalgic or academic.

The platform has a coherent common structure while allowing projects and media to retain distinct character. Metropolitan Trails may use a stronger urban-research vocabulary; other projects may center nature, travel, craft, memory, bodily experience, or other forms of outdoor learning.

Key visual principles:

- Content leads; the first viewport shows the learning field already in use.
- Different media may have different forms instead of being forced into identical cards.
- Relationships between contributions are visible and actionable.
- The interface avoids the authority and rigidity of an institutional learning-management system.
- Research labels, coordinates, and filing devices are used selectively so casual contributors do not feel they must behave like professional researchers.
- The defining idea is: **the world itself is the school.**

## 4. Core Content Model

### Person

A person has a simple profile focused on contributions, projects, and knowledge relationships rather than follower counts or popularity.

### Share

A Share is the lightest publishing unit. Its author may optionally select one of four types: **story**, **learning reflection**, **question**, or **material**. If no type is selected, it is stored as material. A Share can contain:

- a story;
- a learning reflection;
- a question;
- an observation;
- text, photographs, audio, video, files, or links;
- a GIS or other external work represented by a link;
- optional topics;
- an optional place name and coordinates;
- optional association with one or more projects.

Only a title or body is required for initial publishing. Media, topics, locations, and project associations can be added later.

### Connection

A Connection relates one Share to another. Initial relationship types are:

- response;
- addition;
- reference;
- extension.

A connected contribution remains a first-class Share rather than becoming a subordinate comment. This allows it to be discovered, related again, and included in projects.

### Project

A Project is a persistent, evolving learning space. It contains:

- a name and short description;
- an initiator and participants;
- collected Shares;
- simple offline activity information;
- questions, external works, and evolving outcomes represented as collected Shares.

A project may remain openly unfinished or exploratory. Creating one requires only a name, description, and initiator. Any authenticated pilot participant can join a Project without approval. Members may add Shares and simple Activity items. Only the initiator can edit Project identity and description or remove a member.

### Project membership and collection

A Share may be collected by more than one Project. Any Project member can collect any Share visible within the pilot. The association never copies or transfers ownership of the Share. The Share's author can remove their Share from any Project, and the Project initiator can remove any Project association. The first pilot has no proposal or approval state.

### Activity

An offline Activity is represented as a simple Project item with time, place, description, preparation notes, and optional accessibility or safety information. Registration, capacity management, and attendance tracking are not part of the first release.

The Activity creator and Project initiator may edit or delete an Activity. Other Project members may create and view Activities but cannot modify someone else's Activity.

## 5. Information Architecture

The first release has six primary surfaces:

1. **Open Field home** — a communal view of current Shares, Projects, and simple upcoming activities.
2. **Create Share** — a low-friction publishing surface with optional enrichment.
3. **Share detail** — the full material, its author and metadata, visible Connections, and actions to respond or include it in a Project.
4. **Project detail** — project identity, participants, collected Shares, open questions, external works, and activity information.
5. **Create/edit Project** — minimal project setup followed by incremental enrichment.
6. **Person profile** — a person's Shares, Projects, and meaningful Connections.

The home surface is not a map or a project directory. It is a shared working field that directly presents what participants are observing, learning, making, and asking.

Discovery in the small pilot uses:

- a complete chronological view of recent contributions;
- simple filters for content type, topic, and Project;
- direct links among connected Shares;
- optional place labels;
- Projects as durable anchors.

A map may later become one peer view among list, timeline, and relationship views. It is not the platform's organizing backbone. In the first release, GIS works keep their own expressive form through links to their source.

## 6. Primary Interaction Flows

### Publish a Share

1. A persistent “Add material” action opens a blank composition surface.
2. The participant writes a title or body and may attach media or a link.
3. The Share is published immediately.
4. The platform then offers optional topics, location, Connections, and association with Projects the participant has joined.

Classification follows expression rather than blocking it.

### Respond with knowledge

1. A participant opens a Share and chooses to respond.
2. They select a relationship type: response, addition, reference, or extension.
3. They create a new Share.
4. The new Share is visible to all authenticated pilot participants in its own right and visibly connected to the source.

### Grow a Project

1. A participant creates a Project with a name and short description.
2. They add existing Shares or publish new Shares within it.
3. Other invited participants may join and contribute.
4. The project may collect question Shares, material Shares containing external-work links, outcome Shares, or simple Activity information over time.

### Move between online and offline

Offline coordination may continue through the group's existing communication tools. Outdoor Universities records the activity context and provides a place for participants to associate any resulting contributions, but it does not require submissions or manage attendance.

## 7. Homepage Composition

The first viewport should demonstrate the platform rather than introduce it through a conventional marketing hero.

- A compact header identifies “Outdoor Universities / Shanghai pilot.”
- A short line explains the premise in plain language.
- A prominent “Add material” action is always easy to find.
- The main field immediately mixes recent stories, questions, media, and Project activity.
- Metropolitan Trails appears as the first mature Project, not as the owner or boundary of the platform.
- Participants can switch among all recent Shares, Projects, and upcoming activity information without entering separate product worlds.

The experience should resemble a shared learning surface rather than an endless engagement feed. No public counts or ranking affordances should visually dominate.

## 8. Technical Architecture

### Recommended stack

- **Application:** Next.js responsive web application
- **Database, authentication, and storage:** Supabase
- **Deployment:** Vercel
- **Content:** lightweight rich text plus file upload and external links; arbitrary third-party embeds are excluded from the first release

### Principal data entities

- `profiles`
- `shares`
- `share_assets`
- `connections`
- `projects`
- `project_members`
- `project_shares`
- `project_activities`
- `topics`
- `share_topics`
- optional location fields on Shares and Activities

Connections reference a source Share, a target Share, a relationship type, and the participant who created the relation. Project collection uses a join entity so a Share can belong to multiple Projects.

### Data flow

The browser reads pilot content only after authentication through server-rendered or cached application routes. Authenticated mutations create and update Shares, Connections, Projects, memberships, and files through server-side application boundaries backed by Supabase row-level policies.

The first pilot needs only simple authorization:

- only invited, authenticated participants can read pilot content;
- a participant can edit their own profile and edit or delete their own Shares;
- Project initiators can edit Project information;
- any pilot participant can self-join a Project;
- Project members can add Shares and Activity items;
- a Share author can remove their Share from a Project;
- only the Project initiator can edit Project metadata or remove Project members.
- only the Project initiator can delete the Project.

### Invitation lifecycle

The founder sends single-use email invitations from the Supabase administration dashboard; invitation management does not require an application screen in the first release. An invitation expires after seven days. Opening a used, invalid, or expired invitation shows a clear explanation and directs the participant to contact the founder for a new invitation.

Participants cannot delete their profile or authentication account inside the first-release application. The founder may remove an account through Supabase administration after deciding how to handle its authored content and initiated Projects; account self-deletion is outside this specification.

### Deletion semantics

Deleting a Share is permanent after confirmation. It deletes the Share's uploaded assets and removes its Project associations. Connections in which it is either source or target are also removed; independently authored connected Shares remain available. Deleting a Project is permanent after confirmation and removes membership, Activity, and Project-Share association records without deleting the underlying Shares.

## 9. Resilience and Empty States

- Composition autosaves a local draft so navigation or a failed upload does not erase writing.
- Individual media uploads can be retried without clearing the text.
- External works appear as clear, accessible source links; the first release does not attempt arbitrary embeds.
- Destructive actions require confirmation.
- Loading and failure states preserve already-visible content where possible.
- Metropolitan Trails seed content prevents the initial home and Project surfaces from being empty.
- Empty personal and Project sections explain the next meaningful action without gamified pressure.

## 10. Functional Verification

Verification is about reliability and clarity, not participant activity metrics.

Automated and manual checks should cover:

- accepting an invitation and creating or editing a profile;
- publishing, editing, and deleting a text Share;
- publishing a Share with an image, file, or external link;
- recovering a local draft after interruption;
- retrying a failed media upload;
- creating a connected Share from another Share;
- creating a Project and collecting an existing Share;
- showing the same Share correctly in multiple Projects;
- self-joining a Project and allowing only the initiator to remove a member;
- allowing a Share author or Project initiator, but not another member, to remove a Project-Share association;
- allowing only the Project initiator to delete a Project;
- adding and viewing simple Project activity information;
- enforcing basic ownership and Project editing permissions;
- usable keyboard navigation and labels;
- readable layouts on representative mobile and desktop widths.

The pilot should also be observed qualitatively for confusion around the distinction between Shares, Connections, and Projects. This is product-design feedback, not an activation or retention target.

## 11. Initial Content and Rollout

Before invitations are sent, the founder prepares:

- the Metropolitan Trails Project page;
- five to ten real contributions at varied levels of completion;
- a mixture of project context, reading reflections, urban observations, questions, images, links, or route material;
- one simple offline investigation entry if an activity is already planned.

The pilot runs with fewer than ten invited participants. The purpose is to establish whether the framework can comfortably hold real contributions, relationships, and projects. It does not need to demonstrate growth, sustained activity, or the creation of a second Project.

## 12. Future Possibilities, Not Commitments

Future work may explore richer geographic views, relationship graphs, public access, moderation, multilingual use, event registration, group communication, or broader city organization. None of these should shape the first release unless evidence from the pilot makes the need concrete.
