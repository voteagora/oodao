# On & Offchain Attestation DAO Protocol v0.2.0

**Status:** Draft  
**Version:** 0.2.0  
**Depends on:** [Ethereum Attestation Service (EAS)](https://attest.sh/)  

---

## 1. Overview

This protocol defines a set of **attestations** for DAO creation and governance, leveraging the **Ethereum Attestation Service (EAS)**.  

The goals are:  
- Provide a **lightweight, open standard** for representing DAOs and their activities.  
- Make attestations **portable** between platforms.  
- Minimize permissioning, while still allowing **explicit authority delegation** through grants.  

Attestations may be issued **onchain** (with optional custom resolvers) or **offchain** (signed payloads).  

---

## 2. Principles

- **Open Source**: Anyone can implement, extend, or interpret.  
- **Permissioned by Grants**: Authority comes from `GRANT` attestations.  
- **Minimal Enforcement**: Most logic is left to indexers/clients; onchain resolvers are optional.  
- **Composability**: DAOs, roles, proposal types, and votes are linked by `dao_uuid` and proposal UUIDs.  

---

## 3. Attestation Types

### 3.1 `INSTANTIATE`

**Issuer:** A recognized platform (e.g. Agora).
**Purpose:** Declare the DAO and assign its initial authority.
**Revokable:** False.

**Recipient:** `dao_uuid` (`address`) - Unique identifier for this DAO.  The client is expected to instantiate this, and avoid collissions.
**refUID:** `0x0` (discarded, returns `bytes32` attestation UID)

**Schema Fields:**
- `protocol_version` (`uint8`): Version of the protocol spec (for forwards compatibility).
- `name` (`string`): Human-readable name of the DAO.
- `voting_period` (`uint32`): Default voting period duration in seconds.
- `voting_delay` (`uint32`): Default delay before voting begins in seconds.  

---

### 3.2 `PERMA_INSTANTIATE`

**Issuer:** A recognized platform (e.g. Agora).
**Purpose:** Permanently declare the DAO and assign its initial authority. Unlike INSTANTIATE, this version is immutable.
**Revokable:** False.

**Recipient:** `dao_uuid` (`address`) - Unique identifier for this DAO.
**refUID:** `0x0` (discarded, returns `bytes32` attestation UID)

**Schema Fields:**
- `protocol_version` (`uint8`): Version of the protocol spec (for forwards compatibility).
- `name` (`string`): Human-readable name of the DAO.
- `voting_period` (`uint32`): Default voting period duration in seconds.
- `voting_delay` (`uint32`): Default delay before voting begins in seconds.

---

### 3.3 `GRANT`

**Issuer:** Anyone (unguarded), but valid only if the issuer has authority.  
**Purpose:** Assign permissions to subjects within a DAO.  
**Revokable:** True.

**Recipient:** `dao_uuid` (`address`) - Target DAO.
**refUID:** `0x0` (discarded, returns `bytes32` attestation UID)

**Schema Fields:**
- `verb` (`address`): Address being granted permissions.
- `permission` (`string`): One of: `"GRANT"`, `"CREATE_PROPOSAL_TYPE"`, `"CREATE_PROPOSAL"`.
- `level` (`uint8`): Bitmask toggling available powers:
  - Bit 0 (`1`): CREATE
  - Bit 1 (`2`): REVOKE
  - Bit 2 (`4`): UNDO
  Example: `7` (binary `111`) grants create, revoke, and undo.
- `filter` (`string`): JSON string for further granularity (e.g., restrict `GRANT` to certain subsets).  

---

### 3.4 `CREATE_PROPOSAL_TYPE`

**Issuer:** Anyone (unguarded), ignored if permissions aren’t set.  
**Purpose:** Define proposal classes for the DAO.  
**Revokable:** True.

**Recipient:** `dao_uuid` (`address`) - Target DAO.
**refUID:** `0x0` (returns `bytes32` proposal_type_uid)

**Schema Fields:**
- `class` (`string`): Proposal class. Supported values: `"standard"`, `"approval"`, `"optimistic"`.
- `kwargs` (`string`): JSON payload of keyword arguments used when creating proposals.  

---

### 3.5 `CREATE_PROPOSAL`

**Issuer:** Anyone (unguarded), but valid only if the issuer has `CREATE_PROPOSAL` permissions.  
**Purpose:** Submit a proposal under a DAO-defined type.  
**Revocable:** True.

**Recipient:** `dao_uuid` (`address`) - Target DAO.
**refUID:** `proposal_type_uid` or `0x0` if no type specified

**Schema Fields:**
- `proposal_id` (`uint256`): Unique identifier for this proposal.
- `title` (`string`): Proposal title.
- `description` (`string`): Proposal description.
- `startts` (`uint64`): Start timestamp.
- `endts` (`uint64`): End timestamp.
- `tags` (`string`): Tags for categorizing the proposal.  

---

### 3.6 `SET_PROPOSAL_TYPE`

**Issuer:** Anyone (unguarded), but valid only if the issuer has appropriate permissions.
**Purpose:** Associate a proposal with a specific proposal type after creation.
**Revocable:** True.

**Recipient:** `dao_uuid` (`address`) - Target DAO.
**refUID:** `proposal_type_uid` - The proposal type to assign

**Schema Fields:**
- `proposal_id` (`uint256`): The proposal to update with a type.

---

### 3.7 `SET_PARAM_VALUE`

**Issuer:** Anyone (unguarded), but valid only if the issuer has appropriate permissions.
**Purpose:** Set or update a named parameter value for the DAO.
**Revocable:** False.

**Recipient:** `dao_uuid` (`address`) - Target DAO.
**refUID:** `0x0` (discarded, returns `bytes32` attestation UID)

**Schema Fields:**
- `param_name` (`string`): The name of the parameter to set.
- `param_value` (`uint256`): The numeric value to assign to the parameter.

---

### 3.8 `SIMPLE_VOTE`

**Issuer:** Anyone (unguarded). Proposal type must define membership validity check.  
**Purpose:** Record a vote with a simple numeric choice.  
**Revocable:** False.

**Recipient:** `dao_uuid` (`address`) - Target DAO.
**refUID:** `0x0` (discarded, returns `bytes32` attestation UID)

**Schema Fields:**
- `proposal_id` (`uint256`): The proposal being voted on.
- `voter` (`address`): Address casting the vote.
- `choice` (`int8`): e.g. `1 = For`, `-1 = Against`, `0 = Abstain`.
- `reason` (`string`): Optional reason for the vote.  

---

### 3.9 `ADVANCED_VOTE`

**Issuer:** Anyone (unguarded). Proposal type must define membership validity check.  
**Purpose:** Record a vote with a JSON-encoded choice payload.  
**Revocable:** False.

**Recipient:** `dao_uuid` (`address`) - Target DAO.
**refUID:** `0x0` (discarded, returns `bytes32` attestation UID)

**Schema Fields:**
- `proposal_id` (`uint256`): The proposal being voted on.
- `voter` (`address`): Address casting the vote.
- `choice` (`string`): JSON payload relevant to the proposal type.
- `reason` (`string`): Optional reason for the vote.  

---

### 3.10 `UNDO`

**Issuer:** Anyone (unguarded), but interpreted only if issuer has `UNDO` permissions.  
**Purpose:** Retroactively nullify an attestation as if it never occurred. Different from revoke, which applies prospectively.  
**Revocable:** False.

**Recipient:** `dao_uuid` (`address`) - Target DAO.
**refUID:** `uid_of_attestation_to_undo` - The attestation to nullify

**Schema Fields:**
- `verb` (`string`): The action verb describing what's being undone.  

---

## 4. Timestamps

All timestamps, unless otherwise noted, are POSIX, in seconds after 1970 UTC, and are assumed to have infinite trailing zeros of precision.

Attestations must be included in blocks with timestamps before the prevailing timestamp.  Timestamps don't split blocks.

---

## 5. Security Considerations

- **Grant Validation**: Offchain services must verify that a grantor has valid authority before interpreting a `GRANT`.  
- **Undo Semantics**: `UNDO` retroactively invalidates attestations; downstream consumers must handle cascading effects.  
- **Custom Resolvers**: Optional resolvers can enforce invariants (e.g., valid proposal class, timestamp order) onchain.  

---

## 6. Example Flow

1. **DAO Creation**  
   - Agora issues `INSTANTIATE`.  
   - Super-admin address can immediately issue `GRANT`s.  

2. **Role Assignment**  
   - Super-admin grants `CREATE_PROPOSAL_TYPE` to Council members.  

3. **Proposal Lifecycle**  
   - A Council member issues `CREATE_PROPOSAL_TYPE`.  
   - A delegate creates a proposal (`CREATE_PROPOSAL`).  
   - Members vote (`SIMPLE_VOTE` or `ADVANCED_VOTE`).  
   - Results tallied offchain (or onchain with resolver logic).  

4. **Undo**  
   - If a proposal was created fraudulently, an authorized actor can issue `UNDO` on its UID.  

