# Outdoor Universities MVP Implementation Plan

> **For agentic workers:** REQUIRED: Use $subagent-driven-development (if subagents available) or $executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build an invitation-only, mobile-first Outdoor Universities pilot where fewer than ten participants can publish Shares, connect knowledge, create and join Projects, and record simple Project Activities.

**Architecture:** Use a Next.js App Router application with server components for reads and server actions for authenticated mutations. Supabase provides cookie-based authentication, Postgres, private file storage, and row-level authorization; database migrations and seed data remain reproducible in the repository. Feature folders own their schemas, data access, mutations, UI, and tests, while shared platform utilities remain small and explicit.

**Tech Stack:** Next.js, React, TypeScript, CSS Modules plus global design tokens, Supabase (`@supabase/supabase-js`, `@supabase/ssr`, CLI), Zod, Vitest, Testing Library, Playwright, axe-core, Vercel.

**Specification:** `docs/superpowers/specs/2026-07-30-outdoor-universities-design.md`

**Product context:** `PRODUCT.md`

**Current workspace constraint:** This directory is not yet a Git repository. Before implementation begins, obtain the user's approval to initialize Git here. The frequent commit steps below depend on that approval.

**Official references:**

- Next.js installation and App Router: <https://nextjs.org/docs/app/getting-started/installation>
- Supabase SSR authentication: <https://supabase.com/docs/guides/auth/server-side>
- Supabase SSR client setup: <https://supabase.com/docs/guides/auth/server-side/creating-a-client?framework=nextjs&queryGroups=framework>
- Supabase local migrations: <https://supabase.com/docs/guides/local-development/overview>
- Supabase database testing: <https://supabase.com/docs/guides/local-development/testing/overview>

---

## File and Module Map

```text
app/
  (auth)/
    accept-invite/page.tsx           Invitation landing and auth errors
    auth/confirm/route.ts             Supabase email callback
  (pilot)/
    layout.tsx                        Authenticated pilot shell
    page.tsx                          Open Field home
    shares/new/page.tsx               Share composer
    shares/[shareId]/page.tsx         Share detail and Connections
    shares/[shareId]/edit/page.tsx    Owner-only Share editing
    projects/new/page.tsx             Minimal Project creation
    projects/[projectId]/page.tsx     Project detail, membership, collection, Activities
    people/[profileId]/page.tsx       Person profile
  globals.css                         Open Field tokens and global rules
  layout.tsx                          Root document shell
  error.tsx                           Recoverable route error
  not-found.tsx                       Missing/private content state

components/
  app-shell.tsx                       Navigation and persistent Add Material action
  empty-state.tsx                     Shared quiet empty state
  media-attachment.tsx                Image/file/link presentation
  field-grid.tsx                      Responsive mixed-media home composition

features/
  auth/
    actions.ts                        Sign out and profile completion
    guards.ts                         Require authenticated profile
  profiles/
    schema.ts                         Profile input validation
    queries.ts                        Profile reads
    actions.ts                        Profile updates
    profile-form.tsx                  Profile editor
  shares/
    schema.ts                         Share and attachment validation
    queries.ts                        Home/detail/profile Share reads
    actions.ts                        Create/edit/delete Share and upload metadata
    repository.ts                     Supabase persistence boundary for Share actions
    share-card.tsx                    Media-aware Share summary
    share-composer.tsx                Draft-aware composition UI
    share-detail.tsx                  Full Share material
  connections/
    schema.ts                         Relationship validation
    queries.ts                        Incoming/outgoing Connection reads
    actions.ts                        Create connected Share
    repository.ts                     Atomic connected-Share RPC boundary
    connection-composer.tsx           Response/addition/reference/extension flow
  projects/
    schema.ts                         Project, membership, collection validation
    queries.ts                        Project reads
    actions.ts                        Create/join/edit/delete/collect/remove
    repository.ts                     Project persistence boundary
    project-header.tsx                Identity and membership actions
    project-form.tsx                  Create/edit Project fields
    project-members.tsx               Join and initiator-only member controls
    project-collection.tsx            Collected Shares
    project-share-picker.tsx          Search and collect pilot Shares
  activities/
    schema.ts                         Activity validation
    queries.ts                        Upcoming and Project Activity reads
    actions.ts                        Create/edit/delete Activity
    repository.ts                     Activity persistence boundary
    activity-form.tsx                 Create/edit Activity fields
    activity-list.tsx                 Project Activity presentation
    activity-actions.tsx              Permission-aware edit/delete controls
  topics/
    queries.ts                        Topic/filter reads

lib/
  env.ts                              Runtime environment validation
  result.ts                           Typed success/error result
  supabase/
    browser.ts                        Browser client
    server.ts                         Cookie-aware server client
    proxy.ts                          Session refresh helper
  uploads/
    constraints.ts                    Canonical MIME and size limits created with storage migration
    local-draft.ts                    Browser draft persistence

supabase/
  config.toml                         Local services, auth, private bucket
  migrations/
    202607300001_initial_schema.sql   Tables, indexes, triggers
    202607300002_rls.sql              RLS policies and helper functions
    202607300003_storage.sql          Private bucket and object policies
    202607300004_domain_functions.sql Atomic Project and connected-Share functions
  seed.sql                            Pilot users and Metropolitan Trails content
  tests/
    database/
      schema.test.sql                 Constraints and cascades
      rls.test.sql                    Read/write authorization

tests/
  setup.ts                            DOM test environment
  factories.ts                       Typed test fixtures
  unit/
    shares/schema.test.ts
    connections/schema.test.ts
    projects/schema.test.ts
    activities/schema.test.ts
    local-draft.test.ts
  components/
    share-composer.test.tsx
    connection-composer.test.tsx
    project-membership.test.tsx
  e2e/
    helpers/auth.ts                   Deterministic local invite/session fixture
    invitation.spec.ts
    share-flow.spec.ts
    connection-flow.spec.ts
    project-flow.spec.ts
    profile-flow.spec.ts
    responsive-a11y.spec.ts

proxy.ts                              Protect pilot routes and refresh auth
vitest.config.ts
playwright.config.ts
.env.example
DESIGN.md                             Durable Open Field design system
README.md                             Local setup, seed, tests, deployment
```

Boundaries:

- UI files call feature actions and queries; they do not instantiate Supabase clients directly.
- Feature actions validate with Zod and return `ActionResult<T>`.
- Queries return view models rather than raw database rows.
- Authorization is enforced in Postgres RLS; server actions also perform friendly precondition checks.
- Activities remain subordinate to Projects. They do not become a general event subsystem.
- External works are links only in this release.

---

## Chunk 1: Reproducible Foundation

### Task 1: Initialize the repository and application toolchain

**Files:**

- Create: `.gitignore`
- Create: `package.json`
- Create: `pnpm-lock.yaml`
- Create: `tsconfig.json`
- Create: `next.config.ts`
- Create: `eslint.config.mjs`
- Create: `next-env.d.ts`
- Create: `public/`
- Create: `vitest.config.ts`
- Create: `playwright.config.ts`
- Create: `tests/setup.ts`
- Create: `.env.example`
- Create: `app/layout.tsx`
- Create: `app/page.tsx` temporarily, removed when pilot routes land

- [ ] **Step 1: Obtain approval and initialize Git**

Run:

```bash
git init
git branch -M main
```

Expected: an empty repository on branch `main`.

Verify:

```bash
git branch --show-current
```

Expected output: exactly `main`.

- [ ] **Step 2: Scaffold Next.js without overwriting product documents**

Create the scaffold in a disposable directory and copy an explicit allowlist so the existing PDFs, `PRODUCT.md`, and `docs/` cannot be overwritten:

```bash
scaffold_dir="$(mktemp -d)"
pnpm create next-app@latest "$scaffold_dir/app" --ts --eslint --app --src-dir=false --use-pnpm --import-alias="@/*" --yes
cp "$scaffold_dir/app/package.json" .
cp "$scaffold_dir/app/pnpm-lock.yaml" .
cp "$scaffold_dir/app/tsconfig.json" .
cp "$scaffold_dir/app/next.config.ts" .
cp "$scaffold_dir/app/eslint.config.mjs" .
cp "$scaffold_dir/app/next-env.d.ts" .
cp "$scaffold_dir/app/.gitignore" .
cp -R "$scaffold_dir/app/app" .
cp -R "$scaffold_dir/app/public" .
```

Expected: `package.json`, `pnpm-lock.yaml`, `app/`, and `public/` exist; `PRODUCT.md`, `docs/`, and both source PDFs still exist unchanged. Leave the disposable directory for the operating system to clean up; do not use a recursive delete command.

- [ ] **Step 3: Install runtime and test dependencies**

Run:

```bash
pnpm add @supabase/supabase-js @supabase/ssr zod
pnpm add -D vitest @vitejs/plugin-react jsdom @testing-library/react @testing-library/jest-dom @testing-library/user-event @playwright/test @axe-core/playwright supabase
pnpm exec playwright install chromium
```

Expected: exit `0`; `pnpm-lock.yaml` contains `@supabase/ssr`, `vitest`, and `@playwright/test`.

- [ ] **Step 4: Add stable scripts**

Ensure `package.json` contains:

```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "lint": "eslint .",
    "typecheck": "tsc --noEmit",
    "test": "vitest run",
    "test:watch": "vitest",
    "test:e2e": "playwright test",
    "db:start": "supabase start",
    "db:reset": "supabase db reset",
    "db:test": "supabase test db",
    "db:types": "supabase gen types typescript --local > lib/supabase/database.types.ts",
    "verify": "pnpm lint && pnpm typecheck && pnpm test && pnpm build"
  }
}
```

- [ ] **Step 5: Configure Vitest**

`vitest.config.ts`:

```ts
import react from "@vitejs/plugin-react";
import { defineConfig } from "vitest/config";

export default defineConfig({
  plugins: [react()],
  test: {
    environment: "jsdom",
    setupFiles: ["./tests/setup.ts"],
    include: ["tests/**/*.test.{ts,tsx}"],
    coverage: { reporter: ["text", "html"] }
  },
  resolve: { alias: { "@": new URL(".", import.meta.url).pathname } }
});
```

`tests/setup.ts`:

```ts
import "@testing-library/jest-dom/vitest";
```

- [ ] **Step 6: Define environment contract**

`.env.example`:

```dotenv
NEXT_PUBLIC_SUPABASE_URL=http://127.0.0.1:54321
NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY=replace-with-local-publishable-key
NEXT_PUBLIC_SITE_URL=http://localhost:3000
```

Do not put service-role keys in the web application environment.

- [ ] **Step 7: Verify the blank scaffold**

Run:

```bash
pnpm lint
pnpm typecheck
pnpm test --passWithNoTests
pnpm build
```

Expected: ESLint reports zero errors; TypeScript reports zero errors; Vitest reports zero failed tests; Next.js prints `Compiled successfully` and exits `0`.

- [ ] **Step 8: Commit**

```bash
git add .gitignore package.json pnpm-lock.yaml tsconfig.json next.config.ts eslint.config.mjs next-env.d.ts public vitest.config.ts playwright.config.ts tests/setup.ts .env.example app
git commit -m "chore: scaffold outdoor universities web app"
```

### Task 2: Establish the Open Field design system and application shell

**Required skills:** Use `$impeccable` before UI edits. Load its craft floor immediately before editing.

**Files:**

- Create: `DESIGN.md`
- Create: `app/globals.css`
- Create: `components/app-shell.tsx`
- Create: `tests/components/app-shell.test.tsx`
- Modify: `app/layout.tsx`

- [ ] **Step 1: Write the failing shell test**

`tests/components/app-shell.test.tsx`:

```tsx
import { render, screen } from "@testing-library/react";
import { AppShell } from "@/components/app-shell";

it("keeps the add-material action and pilot identity visible", () => {
  render(<AppShell profileName="Lin"><div>Field content</div></AppShell>);
  expect(screen.getByText("Outdoor Universities")).toBeVisible();
  expect(screen.getByText("Shanghai pilot")).toBeVisible();
  expect(screen.getByRole("link", { name: /add material/i })).toHaveAttribute("href", "/shares/new");
  expect(screen.getByText("Field content")).toBeVisible();
});
```

- [ ] **Step 2: Run the test and confirm failure**

Run:

```bash
pnpm vitest run tests/components/app-shell.test.tsx
```

Expected: FAIL because `components/app-shell.tsx` does not exist.

- [ ] **Step 3: Load the Impeccable design context before editing**

Run once from the project root:

```bash
node /Users/jacksoncai/.agents/skills/impeccable/scripts/context.mjs --target app/layout.tsx
```

Read the Impeccable `new-work.md` playbook, resolve the approved Open Field direction against `PRODUCT.md`, then read `reference/craft-floor.md` immediately before the first UI edit. Do not rerun `context.mjs` later in the session. Record and follow every applicable directive; report stale-context warnings without silently repairing them.

- [ ] **Step 4: Write the design contract**

Create `DESIGN.md` with:

- product thesis: the world itself is the school;
- Open Field as the durable visual world;
- mobile-first Operate/Read mode;
- typography roles, color strategy, spacing rhythm, surfaces, media behavior;
- content-led first viewport;
- visible Connections and a persistent Add Material action;
- explicit bans on social popularity chrome, LMS styling, uniform card grids, decorative pseudo-research labels, and inaccessible low contrast;
- reduced-motion and keyboard requirements.

Do not finalize arbitrary tokens before inspecting the first shell at mobile and desktop widths.

- [ ] **Step 5: Implement the minimal accessible shell**

`components/app-shell.tsx`:

```tsx
import Link from "next/link";
import type { ReactNode } from "react";

export function AppShell({
  children,
  profileName
}: {
  children: ReactNode;
  profileName: string;
}) {
  return (
    <div className="app-shell">
      <header className="site-header">
        <Link href="/" className="site-identity">
          <span>Outdoor Universities</span>
          <small>Shanghai pilot</small>
        </Link>
        <nav aria-label="Primary">
          <Link href="/projects">Projects</Link>
          <Link href="/me">{profileName}</Link>
          <Link href="/shares/new" className="add-material">Add material</Link>
        </nav>
      </header>
      <main id="main-content">{children}</main>
    </div>
  );
}
```

Update `app/layout.tsx` to import `./globals.css`, render `<html lang="en">`, and render only `{children}`. `AppShell` belongs in the authenticated `app/(pilot)/layout.tsx` created in Task 4, so authentication pages never inherit pilot navigation.

For this task's visual inspection only, make temporary `app/page.tsx` render `AppShell` with static placeholder children. Task 4 deletes this preview when it creates authenticated `app/(pilot)/page.tsx`; no pilot data is exposed by the preview.

- [ ] **Step 6: Implement tokens and responsive layout**

Use semantic CSS custom properties in `app/globals.css`:

```css
:root {
  --field-bg: #f4f3ed;
  --field-ink: #171916;
  --field-muted: #61665f;
  --field-line: #c9ccc4;
  --field-action: #245f3f;
  --field-paper: #fffef9;
  --space-1: 0.375rem;
  --space-2: 0.75rem;
  --space-3: 1.125rem;
  --space-4: 1.75rem;
  --space-5: 2.75rem;
  --measure: 68rem;
}
```

Treat these values as provisional until browser inspection. Record surviving values in `DESIGN.md`.

- [ ] **Step 7: Verify shell behavior**

Run:

```bash
pnpm vitest run tests/components/app-shell.test.tsx
pnpm lint
pnpm typecheck
```

Expected: `app-shell.test.tsx` reports `1 passed`; ESLint and TypeScript report zero errors.

- [ ] **Step 8: Inspect at 390×844 and 1440×1000**

Start:

```bash
pnpm dev
```

Verify:

- navigation is keyboard reachable;
- Add Material is visible without covering content;
- no horizontal scroll;
- identity remains legible;
- reduced motion does not hide content.

- [ ] **Step 9: Commit**

```bash
git add DESIGN.md app components tests/components/app-shell.test.tsx
git commit -m "feat: establish open field application shell"
```

### Task 3: Create the reproducible Supabase schema, policies, and seed

**Files:**

- Create: `supabase/config.toml`
- Create: `supabase/migrations/202607300001_initial_schema.sql`
- Create: `supabase/migrations/202607300002_rls.sql`
- Create: `supabase/migrations/202607300003_storage.sql`
- Create: `supabase/seed.sql`
- Create: `supabase/tests/database/schema.test.sql`
- Create: `supabase/tests/database/rls.test.sql`
- Create: `lib/supabase/database.types.ts`
- Create: `lib/uploads/constraints.ts`
- Create: `tests/unit/uploads/constraints-parity.test.ts`

- [ ] **Step 1: Initialize local Supabase**

Run:

```bash
pnpm supabase init
```

Expected: `supabase/config.toml` is created.

- [ ] **Step 2: Lock the exact schema contract**

Implement only these columns in the initial migration; every ID is `uuid primary key default gen_random_uuid()` unless it references an auth user:

| Table | Required columns | Optional columns | Delete behavior |
|---|---|---|---|
| `profiles` | `id uuid primary key references auth.users on delete cascade`, `display_name text`, timestamps | `bio text`, `external_url text` | Auth-user deletion is admin-only and outside the app |
| `shares` | `author_id → profiles restrict`, `kind share_kind default material`, timestamps | `title`, `body`, place and paired coordinates | Profile deletion is blocked until an admin explicitly resolves authored Shares |
| `share_assets` | `share_id → shares cascade`, `owner_id → profiles restrict`, `asset_kind`, timestamps | exactly one of `storage_path` or `external_url`; `mime_type`, `display_name`, `byte_size`, thumbnail metadata | Deleted with Share |
| `connections` | `source_share_id → shares cascade`, `target_share_id → shares cascade`, `creator_id → profiles restrict`, `kind connection_kind`, timestamp | none | Connection disappears when either Share is deleted; the other Share remains |
| `projects` | `initiator_id → profiles restrict`, `name`, `description`, timestamps | none | Only initiator deletes; child associations cascade |
| `project_members` | composite key `(project_id, profile_id)`, both FKs cascade, timestamp | none | Removed with Project; profile account deletion is admin-only |
| `project_shares` | composite key `(project_id, share_id)`, both FKs cascade, `added_by → profiles restrict`, timestamp | none | Removing/deleting Project never deletes Share |
| `project_activities` | `project_id → projects cascade`, `creator_id → profiles restrict`, `title`, `starts_at`, timestamps | description, end, place/coordinates, preparation/accessibility/safety notes | Deleted with Project |
| `topics` | `id`, unique `slug`, `label`, timestamp | none | Retained while referenced |
| `share_topics` | composite key `(share_id, topic_id)`, both FKs cascade | none | Association-only |

Constraints:

- `share_kind`: `story`, `reflection`, `question`, `material`;
- `connection_kind`: `response`, `addition`, `reference`, `extension`;
- `asset_kind`: `upload`, `external_link`;
- Share title and body cannot both be blank;
- source and target Share must differ;
- latitude/longitude are both null or both present and valid;
- Activity end is null or not earlier than start;
- Project names are not globally unique;
- asset row has exactly one of `storage_path` or `external_url`.

- [ ] **Step 3: Write failing pgTAP schema tests**

Test for the exact tables, required foreign keys, Share type constraint, Connection type constraint, duplicate Project names being allowed, cascade behavior, and private `share-assets` bucket.

The file must begin with `select plan(35)` and contain exactly these named assertions before `finish()`:

1. profiles exists;
2. shares exists;
3. share_assets exists;
4. connections exists;
5. projects exists;
6. project_members exists;
7. project_shares exists;
8. project_activities exists;
9. topics exists;
10. share_topics exists;
11–20. required foreign keys: Share author; asset Share and owner; Connection source, target, and creator; Project initiator; Project-Share added-by; Activity Project and creator;
21. Share type accepts only the four enum values;
22. Connection type accepts only the four enum values;
23. asset type accepts only `upload` and `external_link`;
24. blank Share is rejected;
25. self-Connection is rejected;
26. unpaired/invalid coordinates are rejected;
27. Activity end-before-start is rejected;
28. duplicate Project names are allowed;
29. asset has exactly one of storage path or external URL;
30. deleting a Share removes assets, Connections, and Project associations but preserves the other connected Share;
31. deleting a Project removes memberships, Activities, and Project-Share associations but preserves underlying Shares;
32. private bucket exists;
33. bucket `public` flag is false;
34. bucket limit is 15 MiB;
35. bucket allowed MIME types exactly match the canonical list.

- [ ] **Step 4: Run tests and confirm failure**

Run:

```bash
pnpm db:start
pnpm db:test
```

Expected: pgTAP reports missing `public.shares` and zero migration syntax failures. If Docker is unavailable, stop and report the environment prerequisite rather than treating it as an application defect.

- [ ] **Step 5: Implement the initial schema migration**

Create:

- enums `share_kind`, `connection_kind`, and `asset_kind`;
- tables in the module map;
- `created_at` and `updated_at` timestamps;
- optional `place_name`, `latitude`, `longitude` on Shares and Activities;
- unique `(project_id, profile_id)` membership;
- unique `(project_id, share_id)` collection;
- indexes on chronological feeds, author, Project membership, source/target Connections, and topic joins;
- foreign keys and cascades exactly matching the schema contract table above.

Use one canonical profile trigger:

```sql
create function public.handle_new_user()
returns trigger
language plpgsql
security definer set search_path = ''
as $$
begin
  insert into public.profiles (id, display_name)
  values (new.id, coalesce(new.raw_user_meta_data ->> 'display_name', split_part(new.email, '@', 1)));
  return new;
end;
$$;
```

- [ ] **Step 6: Write failing RLS tests**

Use exactly this policy matrix and test one allowed and one forbidden actor for every mutable row:

| Resource | Select | Insert | Update | Delete |
|---|---|---|---|---|
| profiles | authenticated | own trigger only | own profile | none in app |
| shares | authenticated | author = auth user | author | author |
| share_assets | authenticated | owner and Share author | owner | owner |
| connections | authenticated | creator authenticated and both Shares visible | none | creator or author of source Share |
| projects | authenticated | initiator = auth user | initiator | initiator |
| project_members | authenticated | self-join, or automatic initiator membership RPC | none | self-leave or initiator removes non-initiator |
| project_shares | authenticated | Project member | none | Share author or Project initiator |
| project_activities | authenticated | Project member and creator = auth user | creator or Project initiator | creator or Project initiator |
| topics | authenticated | none in app | none | none |
| share_topics | authenticated | Share author | none | Share author |

Also assert that anonymous users cannot select any application table and that deletion of one connected Share removes only the Connection, not the independently authored other Share.

`rls.test.sql` must use `select plan(67)` with these grouped counts:

- 10 anonymous read denials, one for each application table;
- 10 authenticated read allowances;
- 2 profile ownership assertions;
- 5 Share author/other-actor assertions;
- 3 Share-asset owner/other-actor assertions;
- 4 Connection creator/source-author/other-actor assertions;
- 5 Project initiator/other-actor assertions;
- 5 membership self-join/self-leave/initiator-removal assertions, including rejection of initiator self-leave;
- 5 Project-Share member/author/initiator/other-actor assertions;
- 7 Activity member/creator/initiator/other-actor assertions;
- 4 topic and Share-topic write assertions;
- 2 deletion-preservation assertions.
- 5 private-storage assertions: authenticated read, owner-prefix insert, other-user insert rejection, owner delete, and other-user delete rejection.

- [ ] **Step 7: Implement RLS policies**

Use small SQL helper functions for `is_project_member(project_id)` and `is_project_initiator(project_id)`. Enable RLS on every application table and on storage objects. Do not rely on server-action checks as the security boundary.

- [ ] **Step 8: Define canonical upload constraints and configure private storage**

Create `lib/uploads/constraints.ts` now with the exact 15 MiB limit and MIME list below; repeat the same values in `202607300003_storage.sql`, and add a test that parses both lists and fails when they diverge:

```ts
export const MAX_UPLOAD_BYTES = 15 * 1024 * 1024;
export const ALLOWED_UPLOAD_TYPES = [
  "image/jpeg", "image/png", "image/webp",
  "audio/mpeg", "audio/mp4",
  "video/mp4", "video/webm",
  "application/pdf",
  "text/plain", "text/csv", "application/geo+json",
  "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
  "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
  "application/zip"
] as const;
```

`tests/unit/uploads/constraints-parity.test.ts` reads `202607300003_storage.sql` as text, asserts it contains `15728640`, and loops over `ALLOWED_UPLOAD_TYPES` asserting every MIME string occurs exactly once. Run:

```bash
pnpm vitest run tests/unit/uploads/constraints-parity.test.ts
```

Expected: `1 passed`; changing either list alone fails the named parity test.

Create a private `share-assets` bucket with:

- maximum file size defined in one migration;
- allowed MIME types matching `lib/uploads/constraints.ts`;
- object keys under `<auth-user-id>/<share-id>/<uuid>-<safe-name>`;
- authenticated read access for the pilot;
- owner-only insert/delete.

- [ ] **Step 9: Seed deterministic representative content**

`supabase/seed.sql` uses fixed UUIDs and local-only emails for three auth users and then creates:

- founder profile;
- two participant profiles;
- Metropolitan Trails Project;
- 5–10 Shares spanning all four types;
- one image placeholder stored as a link, not a fabricated uploaded object;
- Connections among Shares;
- one Project Activity.

Use stable IDs so E2E tests can navigate directly. Label all seed content as development/demo material. The seed must be safe to rerun after `db reset`.

- [ ] **Step 10: Reset, test, and generate types**

Run:

```bash
pnpm db:reset
pnpm db:test
pnpm db:types
pnpm vitest run tests/unit/uploads/constraints-parity.test.ts
```

Expected: reset output lists `202607300001_initial_schema.sql`, `202607300002_rls.sql`, and `202607300003_storage.sql` followed by seed completion; `schema.test.sql` reports `35/35`, `rls.test.sql` reports `67/67`, and the upload parity test reports `1 passed`; generated types are non-empty and contain `shares`, `connections`, `projects`, `project_activities`, and the `asset_kind` enum.

- [ ] **Step 11: Commit**

```bash
git add supabase lib/supabase/database.types.ts lib/uploads/constraints.ts tests/unit/uploads/constraints-parity.test.ts
git commit -m "feat: add pilot database schema and policies"
```

---

## Chunk 2: Authentication and Domain Boundaries

### Task 4: Add cookie-based authentication and invitation handling

**Files:**

- Create: `lib/env.ts`
- Create: `lib/supabase/browser.ts`
- Create: `lib/supabase/server.ts`
- Create: `lib/supabase/proxy.ts`
- Create: `proxy.ts`
- Create: `features/auth/guards.ts`
- Create: `app/(auth)/auth/confirm/route.ts`
- Create: `app/(auth)/accept-invite/page.tsx`
- Create: `app/(pilot)/layout.tsx`
- Create: `app/(pilot)/page.tsx` as an authenticated placeholder until Task 6
- Create: `tests/e2e/invitation.spec.ts`
- Create: `tests/e2e/helpers/auth.ts`
- Create: `supabase/templates/invite.html`
- Modify: `supabase/config.toml`
- Delete: `app/page.tsx`

- [ ] **Step 1: Write the failing invitation E2E cases**

Cover:

- unauthenticated `GET /` redirects to `/accept-invite?next=%2F` and never contains seed content;
- a valid local invite callback ends at `/` and renders `Outdoor Universities`;
- a reused callback ends at `/accept-invite?error=invalid-or-expired`;
- an expired or invalid callback renders “Ask the founder for a new invitation.”

Use one token-hash invitation flow end to end. Create `supabase/templates/invite.html` with:

```html
<a href="{{ .SiteURL }}/auth/confirm?token_hash={{ .TokenHash }}&type=invite&next=/">Join Outdoor Universities</a>
```

Point the local invite template in `supabase/config.toml` to this file, set `site_url = "http://localhost:3000"`, `mailer_autoconfirm = false`, and `mailer_otp_exp = 604800`.

`tests/e2e/helpers/auth.ts` uses the local Supabase service-role key only in the Playwright Node process to call `auth.admin.inviteUserByEmail`. It polls `GET http://127.0.0.1:54324/api/v1/mailbox/{encoded-email}` until one message exists, selects the newest message by timestamp, and extracts the first application `/auth/confirm` URL from its HTML. It never imports into application code.

Do not attempt to accelerate server-side token expiry. Instead, verify the seven-day lifetime with a config assertion against `mailer_otp_exp`, and verify the combined `invalid-or-expired` UI branch using a deterministic malformed `token_hash`. The reused-link test consumes one valid URL twice. These four cases reproduce the product behavior without timing dependence.

- [ ] **Step 2: Run and confirm failure**

```bash
pnpm test:e2e tests/e2e/invitation.spec.ts
```

Expected: four tests fail because auth routes/proxy are missing, not because the local database or fixture setup failed.

- [ ] **Step 3: Validate environment variables**

`lib/env.ts`:

```ts
import { z } from "zod";

export const env = z.object({
  NEXT_PUBLIC_SUPABASE_URL: z.string().url(),
  NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY: z.string().min(1),
  NEXT_PUBLIC_SITE_URL: z.string().url()
}).parse(process.env);
```

- [ ] **Step 4: Implement official Supabase SSR clients**

Follow the current `@supabase/ssr` cookie pattern from the official documentation. Maintain separate browser and server constructors. Never expose a service-role key.

- [ ] **Step 5: Implement route protection**

`proxy.ts` refreshes the session and redirects unauthenticated pilot requests to `/accept-invite`. The authenticated pilot layout calls `requireProfile()` and renders `AppShell`.

Use this exact matcher:

```ts
export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico|accept-invite|auth/confirm).*)"]
};
```

Delete the temporary root `app/page.tsx` in the same change and create `app/(pilot)/page.tsx`; Next.js must have exactly one `/` route, and it must be nested under the authenticated layout.

- [ ] **Step 6: Implement callback errors**

The callback reads `token_hash`, `type`, and `next`, validates `type === "invite"`, and calls `supabase.auth.verifyOtp({ token_hash, type: "invite" })`; it does not call `exchangeCodeForSession`. Success redirects to the validated same-origin `next` path, defaulting to `/`. The database trigger always creates the profile. If `requireProfile()` cannot find it, it signs the user out and redirects to `/accept-invite?error=profile-setup` rather than inventing a profile-completion route. Missing, malformed, reused, or rejected tokens redirect to:

```text
/accept-invite?error=invalid-or-expired
```

The page must explain that invitations are single-use, expire after seven days, and can be reissued by the founder.

- [ ] **Step 7: Verify**

```bash
pnpm test:e2e tests/e2e/invitation.spec.ts
pnpm lint
pnpm typecheck
```

Expected: Playwright reports `4 passed`; unauthenticated `/` returns no pilot content; ESLint and TypeScript report zero errors.

- [ ] **Step 8: Commit**

```bash
git add lib features/auth proxy.ts app/'(auth)' app/'(pilot)' supabase/config.toml supabase/templates/invite.html tests/e2e
git commit -m "feat: protect pilot with invitation authentication"
```

### Task 5: Implement typed domain schemas, results, queries, and mutations

**Required skill:** Use `@test-driven-development`.

**Files:**

- Create: `lib/result.ts`
- Create: `features/profiles/schema.ts`, `queries.ts`, `repository.ts`, `actions.ts`
- Create: `features/shares/schema.ts`, `queries.ts`, `repository.ts`, `actions.ts`
- Create: `features/connections/schema.ts`, `queries.ts`, `repository.ts`, `actions.ts`
- Create: `features/projects/schema.ts`, `queries.ts`, `repository.ts`, `actions.ts`
- Create: `features/activities/schema.ts`, `repository.ts`, `actions.ts`
- Create: `supabase/migrations/202607300004_domain_functions.sql`
- Create: `supabase/tests/database/domain_functions.test.sql`
- Create: `tests/unit/shares/schema.test.ts`
- Create: `tests/unit/connections/schema.test.ts`
- Create: `tests/unit/projects/schema.test.ts`
- Create: `tests/unit/activities/schema.test.ts`
- Create: `tests/unit/domain-actions.test.ts`
- Create: `tests/factories.ts`

- [ ] **Step 1: Write failing validation tests**

Required cases:

- Share accepts title-only or body-only, rejects both empty;
- absent Share type defaults to `material`;
- coordinates are both present or both absent and stay within valid ranges;
- links require `https` or `http`;
- Connection cannot target the source Share;
- Project name and description are required and bounded;
- Activity end time cannot precede start time.

- [ ] **Step 2: Run and confirm failures**

```bash
pnpm vitest run tests/unit
```

Expected: FAIL because schemas do not exist.

- [ ] **Step 3: Implement Zod schemas**

Export input types inferred from Zod. Keep presentation-only labels out of schemas.

Canonical result:

```ts
export type ActionResult<T> =
  | { ok: true; data: T }
  | { ok: false; code: "VALIDATION" | "AUTH" | "FORBIDDEN" | "NOT_FOUND" | "STORAGE" | "UNKNOWN"; message: string; fieldErrors?: Record<string, string[]> };
```

- [ ] **Step 4: Run schema tests**

```bash
pnpm vitest run tests/unit
```

Expected: PASS.

- [ ] **Step 5: Write action tests with a Supabase gateway fake**

Define the complete action contracts before implementation:

```ts
updateProfile(input): Promise<ActionResult<void>>
createShare(input): Promise<ActionResult<{ id: string }>>
updateShare(id, input): Promise<ActionResult<void>>
deleteShare(id): Promise<ActionResult<void>>
addShareAsset(shareId, input): Promise<ActionResult<{ id: string }>>
removeShareAsset(assetId): Promise<ActionResult<void>>
createConnectedShare(sourceId, connectionKind, input): Promise<ActionResult<{ shareId: string }>>
createProject(input): Promise<ActionResult<{ id: string }>>
updateProject(projectId, input): Promise<ActionResult<void>>
deleteProject(projectId): Promise<ActionResult<void>>
joinProject(projectId): Promise<ActionResult<void>>
leaveProject(projectId): Promise<ActionResult<void>>
removeProjectMember(projectId, profileId): Promise<ActionResult<void>>
collectShare(projectId, shareId): Promise<ActionResult<void>>
removeProjectShare(projectId, shareId): Promise<ActionResult<void>>
createActivity(projectId, input): Promise<ActionResult<{ id: string }>>
updateActivity(activityId, input): Promise<ActionResult<void>>
deleteActivity(activityId): Promise<ActionResult<void>>
```

Test each allowed actor and at least one forbidden actor for ownership-sensitive actions. Test attachment metadata for uploaded objects and external links. Test both valid Project-Share removal actors. Keep deletion-cascade assertions in `supabase/tests/database/schema.test.sql`; fake-based action tests verify result mapping, not Postgres cascades.

- [ ] **Step 6: Define repository interfaces and atomic RPCs**

Each `repository.ts` exports a narrow interface consumed by its action module plus a `createSupabase…Repository()` production implementation. Action factories accept a repository for unit tests and default exported server actions construct the production repository; tests never mock Supabase internals.

`202607300004_domain_functions.sql` defines two `security invoker` RPCs:

1. `create_project_with_initiator(name, description)` inserts the Project and initiator membership atomically and returns Project ID.
2. `create_connected_share(source_id, connection_kind, share_input_json)` inserts the target Share and Connection atomically and returns target Share ID.

Inside the pgTAP transaction, create a test-only trigger function that raises `test forced child failure`. Attach it first to `connections before insert`, call the RPC inside `throws_ok`, and assert no target Share with the test marker exists. Drop that trigger, attach the same function to `project_members before insert`, call the Project RPC inside `throws_ok`, and assert no Project with the test marker exists. The surrounding pgTAP transaction rolls back the test-only trigger and function.

`domain_functions.test.sql` uses `select plan(6)`:

1. connected-Share RPC returns a target ID and creates exactly one Connection;
2. forced Connection trigger failure raises the expected exception;
3. forced Connection trigger failure leaves no target Share;
4. Project RPC returns a Project ID with exactly one initiator membership;
5. forced membership trigger failure raises the expected exception;
6. forced membership trigger failure leaves no Project.

- [ ] **Step 7: Implement queries and actions**

Use server-only modules. Convert Supabase errors to stable result codes. Revalidate only affected routes. Do not put authorization logic solely in TypeScript; RLS remains authoritative.

- [ ] **Step 8: Verify**

```bash
pnpm test
pnpm db:reset
pnpm db:test
pnpm db:types
pnpm lint
pnpm typecheck
```

Expected: all schema tests and `domain-actions.test.ts` pass with zero failures; `domain_functions.test.sql` reports `6/6` with zero orphan Shares or Projects; regenerated types contain `create_connected_share` and `create_project_with_initiator` under `Functions`; ESLint and TypeScript report zero errors.

- [ ] **Step 9: Commit**

```bash
git add lib/result.ts lib/supabase/database.types.ts features tests/unit tests/factories.ts supabase/migrations/202607300004_domain_functions.sql supabase/tests/database/domain_functions.test.sql
git commit -m "feat: add typed pilot domain boundaries"
```

---

## Chunk 3: Participant Surfaces

### Task 6: Build the Open Field home and media-aware Share cards

**Files:**

- Create: `components/field-grid.tsx`
- Create: `components/media-attachment.tsx`
- Create: `features/shares/share-card.tsx`
- Modify: `app/(pilot)/page.tsx`
- Create: `features/activities/queries.ts`
- Create: `tests/components/share-card.test.tsx`
- Create: `tests/e2e/responsive-a11y.spec.ts`

- [ ] **Step 1: Write failing component tests**

Verify:

- each Share kind has a visible text label;
- image, file, and link summaries differ semantically;
- no like, follower, view, or ranking counts render;
- author, time, Project associations, and Connection affordance remain accessible.
- chronological order is newest-first;
- combined `kind`, `topic`, and `project` URL filters return their intersection and preserve valid query parameters.

- [ ] **Step 2: Confirm failure**

```bash
pnpm vitest run tests/components/share-card.test.tsx
```

Expected: FAIL because `share-card.tsx`, `field-grid.tsx`, and the home query implementation do not exist; Vitest itself starts successfully.

- [ ] **Step 3: Implement Share view models and cards**

Use media-driven variants without changing reading order:

```ts
type ShareCardView = {
  id: string;
  kind: "story" | "reflection" | "question" | "material";
  title: string | null;
  excerpt: string | null;
  author: { id: string; displayName: string };
  createdAt: string;
  primaryAsset: ImageAsset | FileAsset | LinkAsset | null;
  projects: Array<{ id: string; name: string }>;
  connectionCount: number;
};
```

- [ ] **Step 4: Implement the home field**

Server-render all recent Shares for the pilot. Add URL-based filters for kind, topic, and Project. Keep chronological order. Projects and simple upcoming Activities appear as distinct field items, not injected advertisements.
Read upcoming Activities through `features/activities/queries.ts`; the page must not instantiate Supabase directly.

- [ ] **Step 5: Inspect the real render**

At 390×844 and 1440×1000 verify:

- the first viewport contains real seed material and Add Material;
- different media read distinctly without becoming a masonry accessibility trap;
- filter controls wrap cleanly;
- keyboard order matches visual order;
- no generic dashboard card grid or LMS styling appears.

- save Playwright screenshots to `test-results/visual/home-mobile.png` and `test-results/visual/home-desktop.png` for the final visual review.

- [ ] **Step 6: Verify**

```bash
pnpm vitest run tests/components/share-card.test.tsx
pnpm test:e2e tests/e2e/responsive-a11y.spec.ts
pnpm lint
pnpm typecheck
```

Expected: Share-card/filter tests and responsive accessibility tests pass with zero failures; axe reports zero serious or critical violations; ESLint and TypeScript report zero errors.
Both screenshot files must exist and have non-zero size.

Run:

```bash
test -s test-results/visual/home-mobile.png
test -s test-results/visual/home-desktop.png
```

Expected: both commands exit `0`.

- [ ] **Step 7: Commit**

```bash
git add app/'(pilot)'/page.tsx components features/shares features/activities/queries.ts tests
git commit -m "feat: build the open field home"
```

### Task 7: Build Share composition, upload recovery, and Share detail

**Files:**

- Modify: `lib/uploads/constraints.ts`
- Create: `lib/uploads/local-draft.ts`
- Create: `features/shares/share-composer.tsx`
- Create: `features/shares/share-detail.tsx`
- Create: `app/(pilot)/shares/new/page.tsx`
- Create: `app/(pilot)/shares/[shareId]/page.tsx`
- Create: `app/(pilot)/shares/[shareId]/edit/page.tsx`
- Create: `tests/unit/local-draft.test.ts`
- Create: `tests/components/share-composer.test.tsx`
- Create: `tests/e2e/share-flow.spec.ts`
- Create: `tests/integration/share-storage.test.ts`
- Modify: `features/shares/actions.ts`
- Modify: `features/shares/repository.ts`

- [ ] **Step 1: Write failing draft and composer tests**

Cover:

- title-only and body-only submission;
- type defaults to material;
- optional metadata does not block publishing;
- local draft persists and clears only after confirmed success;
- failed upload leaves text and other successful uploads intact;
- owner can load, edit, and persist an existing text Share;
- non-owner receives not-found from the edit route without leaked content;
- invalid file shows a specific message;
- destructive delete requires confirmation.

- [ ] **Step 2: Confirm failure**

```bash
pnpm vitest run tests/unit/local-draft.test.ts tests/components/share-composer.test.tsx
```

Expected: FAIL because local-draft and composer modules do not exist, not because Vitest configuration fails.

- [ ] **Step 3: Implement draft storage**

Use a versioned key:

```ts
const DRAFT_KEY = "outdoor-universities:share-draft:v1";
```

Persist only text and local metadata, not `File` blobs. Announce restoration and provide a discard action.

- [ ] **Step 4: Reuse and test upload constraints**

Import the canonical MIME list and 15 MiB limit created in Task 3. Add parameterized tests for every allowed type, one unsupported type, a 15 MiB file, and a file one byte over the limit. Do not redefine the list in the composer.

- [ ] **Step 5: Implement the composer**

The first visible state contains title, body, media/link, and Publish. Type, topics, location, Project association, and Connections remain optional progressive disclosure. Project choices include only joined Projects.

- [ ] **Step 6: Implement upload orchestration**

Create the Share first, upload each file to its private path through `shares/repository.ts`, and record successful assets. If an upload fails, return per-file status and retain the Share as a **published text contribution**; there is no database draft status. Keep failed `File` objects in composer state only while the current page remains open, warn before navigation that failed attachments cannot be recovered, and expose per-file retry. Never clear the local text draft until the server confirms the Share and all selected upload states are acknowledged.

`deleteShare` first lists every object under the Share's private storage prefix, deletes those objects, and only then deletes the Share row. If storage deletion fails, return `STORAGE` and preserve the database row. Add a repository integration test asserting no objects remain after successful deletion.

- [ ] **Step 7: Implement detail and ownership actions**

Show full content, source links, location label, topics, Projects, Connections, edit, and delete. The owner-only edit route preloads the Share into the same composer in edit mode and calls `updateShare`; it does not create a new Share. Delete permanently after confirmation and rely on database cascades specified in the migration.

- [ ] **Step 8: Verify**

```bash
pnpm vitest run tests/unit/local-draft.test.ts tests/components/share-composer.test.tsx
pnpm vitest run tests/integration/share-storage.test.ts
pnpm test:e2e tests/e2e/share-flow.spec.ts
pnpm lint
pnpm typecheck
```

Expected: draft/composer tests pass; integration tests prove successful deletion removes storage objects and the Share row, while forced storage failure returns `STORAGE` and preserves the row; Playwright covers create, edit, attachment retry, and delete with zero failures; ESLint and TypeScript report zero errors.

- [ ] **Step 9: Commit**

```bash
git add lib/uploads features/shares app/'(pilot)'/shares tests
git commit -m "feat: add resilient share publishing"
```

### Task 8: Build first-class knowledge Connections

**Files:**

- Create: `features/connections/connection-composer.tsx`
- Create: `tests/components/connection-composer.test.tsx`
- Create: `tests/e2e/connection-flow.spec.ts`
- Modify: `features/connections/actions.ts`
- Modify: `features/connections/repository.ts`
- Modify: `supabase/tests/database/schema.test.sql`
- Modify: `supabase/tests/database/rls.test.sql`
- Modify: `app/(pilot)/shares/[shareId]/page.tsx`
- Modify: `features/shares/share-detail.tsx`

- [ ] **Step 1: Write failing tests**

Verify that a participant can:

- choose response, addition, reference, or extension;
- see the source Share while composing;
- publish a new first-class Share;
- reach the new Share directly from home;
- traverse the Connection in both directions;
- recover safely when either source or target is deleted.

- [ ] **Step 2: Confirm failure**

```bash
pnpm vitest run tests/components/connection-composer.test.tsx
pnpm test:e2e tests/e2e/connection-flow.spec.ts
```

Expected: FAIL because `connection-composer.tsx` and its route integration do not exist; local auth fixtures still initialize successfully.

- [ ] **Step 3: Wire and verify atomic creation**

Call the `create_connected_share` RPC created in Task 5 through `connections/repository.ts`. Database tests must prove: success returns the target Share ID; a forced invalid Connection leaves no target Share; deleting source removes the Connection and preserves target; deleting target removes the Connection and preserves source.

- [ ] **Step 4: Implement visible relationship language**

Use participant-facing labels:

- “Respond with another perspective”
- “Add material”
- “Reference this”
- “Continue this inquiry”

Store stable enum values separately from copy.

- [ ] **Step 5: Verify**

```bash
pnpm vitest run tests/components/connection-composer.test.tsx
pnpm test:e2e tests/e2e/connection-flow.spec.ts
pnpm db:test
pnpm lint
pnpm typecheck
```

Expected: component and E2E Connection tests pass; database tests report zero orphan rows; ESLint and TypeScript report zero errors.

- [ ] **Step 6: Commit**

```bash
git add features/connections features/shares app/'(pilot)'/shares tests supabase/tests/database/schema.test.sql supabase/tests/database/rls.test.sql
git commit -m "feat: make knowledge connections first class"
```

### Task 9: Build Projects, membership, collection, and simple Activities

**Files:**

- Create: `features/projects/project-header.tsx`
- Create: `features/projects/project-form.tsx`
- Create: `features/projects/project-members.tsx`
- Create: `features/projects/project-collection.tsx`
- Create: `features/projects/project-share-picker.tsx`
- Create: `features/activities/activity-form.tsx`
- Create: `features/activities/activity-list.tsx`
- Create: `features/activities/activity-actions.tsx`
- Create: `app/(pilot)/projects/new/page.tsx`
- Create: `app/(pilot)/projects/[projectId]/page.tsx`
- Create: `tests/components/project-membership.test.tsx`
- Create: `tests/e2e/project-flow.spec.ts`
- Modify: `features/projects/actions.ts`
- Modify: `features/projects/repository.ts`
- Modify: `features/activities/actions.ts`
- Modify: `features/activities/repository.ts`
- Modify: `supabase/tests/database/rls.test.sql`

- [ ] **Step 1: Write failing permission and flow tests**

Cover:

- Project creation requires name and description;
- any participant can self-join;
- only initiator edits identity, removes members, or deletes Project;
- members add any pilot Share;
- Share author or initiator removes a Project-Share association;
- the same Share appears in multiple Projects;
- deleting a Project never deletes underlying Shares;
- Activity creator or initiator edits/deletes Activity;
- other members cannot edit that Activity.

- [ ] **Step 2: Confirm failure**

```bash
pnpm vitest run tests/components/project-membership.test.tsx
pnpm test:e2e tests/e2e/project-flow.spec.ts
```

Expected: FAIL because Project membership, collection, and Activity controls do not exist; database setup itself succeeds.

- [ ] **Step 3: Implement minimal Project creation and membership**

Call `create_project_with_initiator` from `projects/repository.ts` so Project creation and initiator membership are atomic. Self-join is immediate. The initiator cannot leave their own Project; they must retain it or delete the Project. `project-form.tsx` owns create/edit fields; `project-members.tsx` owns join/leave and initiator-only removal. Do not add roles beyond initiator/member.

- [ ] **Step 4: Implement Project collection**

`project-share-picker.tsx` searches only authenticated pilot Shares and creates associations; `project-collection.tsx` renders them and permission-aware removal. Each item displays its original author and ownership. Removal changes only the association.

- [ ] **Step 5: Implement Activities as Project items**

Fields:

```ts
{
  title: string;
  description?: string;
  startsAt: string;
  endsAt?: string;
  placeName?: string;
  latitude?: number;
  longitude?: number;
  preparationNotes?: string;
  accessibilityNotes?: string;
  safetyNotes?: string;
}
```

`activity-form.tsx` owns fields and validation; `activity-list.tsx` renders chronological items; `activity-actions.tsx` owns creator/initiator edit and delete. Do not implement registration, capacity, attendance, reminders, or chat.

- [ ] **Step 6: Verify**

```bash
pnpm vitest run tests/components/project-membership.test.tsx
pnpm test:e2e tests/e2e/project-flow.spec.ts
pnpm db:test
pnpm lint
pnpm typecheck
```

Expected: component, E2E, and RLS tests cover every actor in the permission matrix with zero failures; Project deletion preserves Shares; Activity fields render in chronological order; the home upcoming-Activity query returns the created item; ESLint and TypeScript report zero errors.

- [ ] **Step 7: Commit**

```bash
git add features/projects features/activities app/'(pilot)'/projects tests supabase/tests/database/rls.test.sql
git commit -m "feat: add evolving project spaces"
```

### Task 10: Build Person profiles without popularity mechanics

**Files:**

- Create: `features/profiles/profile-form.tsx`
- Create: `app/(pilot)/people/[profileId]/page.tsx`
- Create: `app/(pilot)/me/page.tsx`
- Create: `tests/components/profile-form.test.tsx`
- Create: `tests/e2e/profile-flow.spec.ts`
- Modify: `features/profiles/actions.ts`
- Modify: `features/profiles/queries.ts`

- [ ] **Step 1: Write failing tests**

Verify:

- display name is required;
- bio and optional external link are editable;
- profile shows authored Shares, joined Projects, and Connections;
- follower, view, rank, streak, and activity-score UI is absent;
- account deletion is absent and profile explains that removal requires contacting the founder.

- [ ] **Step 2: Confirm failure**

```bash
pnpm vitest run tests/components/profile-form.test.tsx
```

Expected: FAIL because profile form and routes do not exist; the test environment itself starts successfully.

- [ ] **Step 3: Implement profile views and editing**

Keep profile fields minimal: display name, bio, and optional external link. Do not add avatar upload or social graph tables.

- [ ] **Step 4: Verify**

```bash
pnpm vitest run tests/components/profile-form.test.tsx
pnpm test:e2e tests/e2e/profile-flow.spec.ts
pnpm lint
pnpm typecheck
```

Expected: component tests pass; E2E proves authenticated profile edit persistence and renders authored Shares, joined Projects, and Connections; ESLint and TypeScript report zero errors.

- [ ] **Step 5: Commit**

```bash
git add features/profiles app/'(pilot)'/people app/'(pilot)'/me tests/components/profile-form.test.tsx tests/e2e/profile-flow.spec.ts
git commit -m "feat: add contribution-focused profiles"
```

---

## Chunk 4: Integration, Quality, and Pilot Handoff

### Task 11: Complete error, loading, empty, and not-found states

**Files:**

- Create: `components/empty-state.tsx`
- Create: `app/error.tsx`
- Create: `app/not-found.tsx`
- Create: `app/(pilot)/loading.tsx`
- Create: `tests/components/empty-state.test.tsx`
- Create: `tests/e2e/states.spec.ts`
- Modify: `app/(pilot)/page.tsx`
- Modify: `app/(pilot)/shares/[shareId]/page.tsx`
- Modify: `app/(pilot)/shares/[shareId]/edit/page.tsx`
- Modify: `app/(pilot)/projects/[projectId]/page.tsx`
- Modify: `app/(pilot)/people/[profileId]/page.tsx`
- Modify: `features/shares/share-composer.tsx`
- Modify: `features/projects/project-collection.tsx`
- Modify: `features/activities/activity-form.tsx`

- [ ] **Step 1: Write failing state tests**

`empty-state.test.tsx` contains exactly four component cases:

- empty profile points to Add Material;
- empty Project explains how members add Shares;
- route error offers retry;
- loading skeletons use `aria-busy`, preserve layout, and do not animate under reduced motion.

`states.spec.ts` contains exactly four route/integration cases:

- missing Share calls `notFound()` and exposes no record title;
- forbidden/private Share edit returns the same not-found surface and exposes no record title;
- recoverable route error invokes `reset()` through a visible Retry control;
- Share upload, Project collection, and Activity mutation errors render adjacent to the initiating control while preserving entered values.

- [ ] **Step 2: Confirm failure**

```bash
pnpm vitest run tests/components/empty-state.test.tsx
pnpm test:e2e tests/e2e/states.spec.ts
```

Expected: all eight cases fail because the shared states and route integrations are not implemented; both test runners initialize successfully.

- [ ] **Step 3: Implement shared state components**

Use specific messages and one meaningful next action. Avoid gamification, artificial urgency, and generic “Something went wrong” when a stable error code is available.

The listed dynamic pages call `notFound()` when their query returns `NOT_FOUND` or `FORBIDDEN`; they never render partial record metadata. `app/error.tsx` is a client error boundary that renders a Retry button calling its provided `reset()` function and displays no raw exception or record data.

- [ ] **Step 4: Verify**

```bash
pnpm vitest run tests/components/empty-state.test.tsx
pnpm test:e2e tests/e2e/states.spec.ts
pnpm lint
pnpm typecheck
```

Expected: component suite reports `4 passed`; state E2E reports `4 passed`; ESLint and TypeScript report zero errors.

- [ ] **Step 5: Commit**

```bash
git add components/empty-state.tsx app features tests/components/empty-state.test.tsx tests/e2e/states.spec.ts
git commit -m "feat: complete pilot application states"
```

### Task 12: Seed Metropolitan Trails, verify production behavior, and document handoff

**Required skills:** Use `$impeccable`, `$requesting-code-review`, and `$verification-before-completion`.

**Files:**

- Modify: `supabase/seed.sql`
- Create: `README.md`
- Create: `tests/e2e/pilot-smoke.spec.ts`
- Modify: `DESIGN.md`
- Modify: `.env.example`

- [ ] **Step 1: Replace generic seed copy with approved project material**

Use only content supplied by or accurately summarized from:

- `9aa9bfb1-8f59-4cd4-889a-8862a92ea1c9_用身体来阅读城市-上海城市步道设计.pdf`
- `learning-from-the-trails.pdf`

Clearly label summaries and do not invent participant stories, testimonials, or research outcomes.
Add an Activity only if one is genuinely planned; do not fabricate an event to fill the interface.

- [ ] **Step 2: Write the final smoke test**

Use a dedicated local smoke user `smoke@outdoor-universities.local` that begins outside Metropolitan Trails. Generate names with a run UUID and prefix them `[Smoke]`. One authenticated session must:

1. load the populated Open Field;
2. open Metropolitan Trails;
3. publish a Share;
4. connect a second Share;
5. self-join Metropolitan Trails;
6. collect the first Share;
7. create and then remove an Activity;
8. remove the Share association without deleting the Share.

In `afterEach`, delete the run's Activity, Connection, both Shares, and any temporary Project through the same authorized application APIs, then leave Metropolitan Trails. Assert no `[Smoke]` records with the run UUID remain and the smoke user has no Metropolitan Trails membership. Never use a classmate's account or modify their existing material.

- [ ] **Step 3: Run the smoke test and confirm any failure before fixing**

```bash
pnpm test:e2e tests/e2e/pilot-smoke.spec.ts
```

Expected: FAIL on the first missing or incorrect integrated behavior, while fixture setup succeeds and cleanup leaves zero run records.

- [ ] **Step 4: Document local and hosted setup**

`README.md` must cover:

- prerequisites: Node, pnpm, Docker-compatible runtime, Supabase CLI;
- environment setup;
- `pnpm db:start`, `pnpm db:reset`, and seed accounts;
- all test and verification commands;
- how the founder sends a single-use seven-day invitation in Supabase;
- how to link and push migrations to the remote project;
- how to configure Vercel environment variables;
- known first-release exclusions.
- a test-evidence table naming the suites that prove invitation/profile editing, Share create/edit/delete, image/file/link publishing, draft recovery, failed-upload retry, multi-Project collection, member removal, Project deletion, forbidden association removal, and ownership restrictions.

- [ ] **Step 5: Run database verification from empty state**

```bash
pnpm db:reset
pnpm db:test
pnpm db:types
git diff --exit-code lib/supabase/database.types.ts
```

Expected: reset and database tests pass; generated types match the committed file.

- [ ] **Step 6: Run full application verification**

```bash
pnpm lint
pnpm typecheck
pnpm test
pnpm test:e2e
pnpm build
```

Expected: every command exits `0`; no tests are skipped unexpectedly. The full suite is the evidence for every named critical behavior; `pilot-smoke.spec.ts` reports one repeatable smoke flow and leaves no `[Smoke]` records.

- [ ] **Step 7: Inspect final desktop and mobile renders**

Inspect at minimum:

- home;
- new Share;
- mixed-media Share detail;
- connected Share detail;
- Metropolitan Trails Project;
- Person profile;
- empty and error states.

Check against `DESIGN.md`, the approved Open Field direction, keyboard navigation, contrast, reduced motion, overflow, and media failure states. Update `DESIGN.md` with only the tokens and behaviors that survived the build.

- [ ] **Step 8: Resolve final Impeccable findings**

Run the Impeccable detector exactly once now that all UI edits are complete:

```bash
node /Users/jacksoncai/.agents/skills/impeccable/scripts/detect.mjs --json app components features
```

Save its JSON output to the task log, fix material findings, and pass the final findings plus screenshots to the required Impeccable finish reviewer. Do not run the detector a second time.

- [ ] **Step 9: Request two-stage review**

Dispatch:

1. a requirements/spec compliance reviewer;
2. an implementation quality reviewer;
3. the required Impeccable finish reviewer with the original request, confirmed design, target routes, `DESIGN.md`, and prior detector findings.

Apply material fixes, then rerun the full verification commands affected by those fixes.

Commit every review-driven change before the handoff commit:

```bash
git add app components features lib supabase tests DESIGN.md
git commit -m "fix: address outdoor universities implementation review"
```

Expected: the review-fix commit succeeds when implementation changes exist. If no review changes were needed, skip this commit; documentation and handoff files remain for Step 10.

- [ ] **Step 10: Commit**

```bash
git add README.md DESIGN.md .env.example supabase/seed.sql tests/e2e/pilot-smoke.spec.ts
git commit -m "docs: prepare outdoor universities pilot handoff"
git status --short
```

Expected: handoff commit succeeds and status is empty before deployment begins.

- [ ] **Step 11: Prepare deployment without silently creating external resources**

Ask the user to provide or authorize:

- a Supabase project;
- a Vercel project;
- production site URL;
- invitation sender settings.

Invoke Vercel reproducibly with `pnpm dlx vercel@latest`. After the user authorizes the named Supabase and Vercel projects, verify Vercel has `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY`, and `NEXT_PUBLIC_SITE_URL` for Preview and Production:

```bash
pnpm supabase link --project-ref <approved-project-ref>
pnpm supabase db push --dry-run
pnpm supabase db push
pnpm dlx vercel@latest env ls
pnpm dlx vercel@latest
```

The first Vercel command creates a preview only. Run hosted smoke against the returned preview URL with a disposable invited smoke account:

```bash
PLAYWRIGHT_BASE_URL=<preview-url> pnpm playwright test tests/e2e/pilot-smoke.spec.ts
```

Only after preview smoke succeeds and the user explicitly approves production deployment:

```bash
pnpm dlx vercel@latest --prod
PLAYWRIGHT_BASE_URL=<production-url> pnpm playwright test tests/e2e/pilot-smoke.spec.ts
```

Do not create, link, or deploy external resources without explicit authorization. Do not use destructive remote resets as recovery; if `db push` fails, inspect migration history, fix the forward migration, rerun `db push --dry-run`, and ask before applying again.

- [ ] **Step 12: Close the post-deployment loop**

If hosted smoke requires any code, config, migration, or documentation fix:

1. apply the fix locally;
2. rerun every affected test plus `pnpm verify`;
3. commit the fix;
4. redeploy the approved target;
5. rerun hosted smoke.

Before handoff:

```bash
git status --short
```

Expected: empty output. Deployment is complete only after the approved hosted target passes smoke and the worktree is clean.
