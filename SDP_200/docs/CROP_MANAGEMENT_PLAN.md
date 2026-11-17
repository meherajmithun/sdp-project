# Crop Management Improvement Plan

This document explains how the Crop Management feature will be improved. It is written as a study guide so a beginner can understand what will be built, why each part is needed, and how the work will be checked.

> Planning status: **Waiting for implementation confirmation**
>
> This document does not mean the feature is finished. Completed work will be marked in `IMPROVEMENTS.md` only after implementation and testing.

## 1. Goal

The current Crop Management page mainly adds crops. The improved page should let users manage the complete crop list from one place.

Users should be able to:

1. View all saved crops.
2. Add a new crop.
3. Edit an existing crop.
4. Delete an unused crop safely.
5. Avoid accidental duplicate crops.
6. Load optional sample crop data.

## 2. Planned page layout

The page will have two main areas.

### Crop form

The form will contain:

- Crop name
- Days to harvest
- Soil type
- Sunlight requirement
- Water requirement
- Crop category
- Season

The form will have these actions:

- **Add Crop:** Save a new crop.
- **Update Crop:** Save changes to the selected crop.
- **Clear Form:** Clear every field and leave editing mode.
- **Load Sample Crops:** Add optional starter data after confirmation.

### Crop table

A scrollable table will display:

- ID
- Crop name
- Days to harvest
- Soil type
- Sunlight
- Water requirement
- Category
- Season

When no crops exist, the page will show a friendly empty message instead of an empty table with no explanation.

## 3. Implementation steps

### Step 1: Create a crop data layer

Create a new file named `crop_data.py`.

This file will keep database work separate from interface code. It will contain operations for:

- Loading all crops
- Finding a crop by ID
- Adding a crop
- Updating a crop
- Deleting a crop
- Checking for duplicate names
- Checking whether finance records use a crop
- Loading sample crops

Keeping database code separate makes it easier to understand, reuse, and test.

### Step 2: Display saved crops

Update `crop_management_feature.py` so that it:

1. Loads crops when the page opens.
2. Displays the crops in a scrollable table.
3. Refreshes the table after a change.
4. Shows the number of saved crops.
5. Shows a useful message when no crops exist.

### Step 3: Validate crop information

Before saving a crop, the app will:

- Remove unnecessary spaces from the name.
- Require a crop name.
- Require harvest days to be a positive whole number.
- Require a value from every dropdown.
- Check names without caring about capitalization.

For example, the following names will be treated as duplicates:

```text
Rice
rice
 RICE
```

Existing duplicate records will still be displayed, but the app will prevent users from creating new duplicates.

### Step 4: Edit a crop

The editing workflow will be:

1. Select a crop in the table.
2. Choose **Edit Selected**.
3. The crop information appears in the form.
4. The page clearly says that the crop is being edited.
5. Choose **Update Crop** to save the changes.
6. The table and related finance pages refresh.

If the crop name changes, finance screens should display the current crop name.

### Step 5: Delete a crop safely

The deletion workflow will be:

1. Select a crop in the table.
2. Choose **Delete Selected**.
3. Read the inline confirmation message.
4. Choose **Confirm Delete** or **Cancel**.

Safety rules:

- A crop will not be deleted without confirmation.
- A crop used by a sale or expense will not be deleted.
- The page will explain why a referenced crop cannot be deleted.
- An unused crop can be deleted normally.

These rules prevent financial records from becoming broken or confusing.

### Step 6: Add optional sample crops

The page will include a **Load Sample Crops** button.

Sample crops will:

- Never load automatically.
- Require user confirmation.
- Skip names that already exist.
- Be safe to load more than once.
- Include useful examples such as rice, wheat, potato, tomato, and maize.

### Step 7: Add automated tests

Create `tests/test_crops.py` with tests for:

- Adding a valid crop
- Rejecting an empty crop name
- Rejecting invalid harvest days
- Preventing duplicate names
- Loading all saved crops
- Editing a crop
- Preventing an edit that creates a duplicate
- Deleting an unused crop
- Blocking deletion of a referenced crop
- Loading sample crops without duplicates

All existing finance tests must continue to pass.

### Step 8: Update the improvement tracker

After implementation and testing:

1. Mark completed subtasks with `[x]` in `IMPROVEMENTS.md`.
2. Mark **2. Improve crop management** complete only when every subtask is done.
3. Add the completion date and final commit to the completed-work log.

## 4. Planned files

```text
SDP_200/
├── crop_data.py
├── crop_management_feature.py
├── finance_ui.py
├── tests/
│   └── test_crops.py
└── docs/
    ├── CROP_MANAGEMENT_PLAN.md
    └── IMPROVEMENTS.md
```

## 5. Small commit plan

Implementation will use small, focused commits without the `feat` prefix:

1. `Add crop data service and tests`
2. `Add crop management table`
3. `Add crop editing`
4. `Add safe crop deletion`
5. `Add optional sample crops`
6. `Complete crop management tracker`

## 6. Completion checklist

The improvement will be considered complete only when:

- [ ] Saved crops appear in the table.
- [ ] Users can add crops.
- [ ] Users can edit crops.
- [ ] Users can safely delete unused crops.
- [ ] Referenced crops cannot be accidentally deleted.
- [ ] Duplicate crops are prevented.
- [ ] Sample data is optional and safe to load repeatedly.
- [ ] All crop tests pass.
- [ ] All existing finance tests pass.
- [ ] `IMPROVEMENTS.md` is updated.
- [ ] The completed changes are pushed to GitHub.

## 7. Important beginner concepts

### Why use crop IDs?

Two crops can sometimes have similar names. A database ID gives every crop a unique identity, so the app always updates or deletes the correct record.

### Why separate database and interface code?

The interface should focus on buttons, forms, tables, and messages. The data layer should focus on saving and loading information. Separating them makes the code easier to read and test.

### Why block deletion of referenced crops?

A sale or expense may point to a crop. Deleting that crop would leave the finance record without a reliable crop. Blocking the deletion protects the data.

### Why test sample-data loading twice?

Users may accidentally press the sample-data button more than once. The operation must skip duplicates instead of adding the same crops repeatedly.
