// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/// @title DaoSchemas v0.2.0
/// @notice Schema definitions for the EAS-Based DAO Protocol v0.2.0
/// @dev These schema strings should be registered on EAS SchemaRegistry.
/// @dev Note: dao_uuid is passed as the recipient parameter, not in the schema.
/// @dev Note: References to other attestations use refUID parameter, not schema fields.

contract DaoSchemasV020 {
    // 1. INSTANTIATE
    // recipient: dao_uuid (address)
    // refUID: 0x0 (discarded, returns bytes32 attestation UID)
    string public constant INSTANTIATE_SCHEMA =
        "uint8 protocol_version,string name,uint32 voting_period,uint32 voting_delay";

    // 2. PERMA_INSTANTIATE
    // recipient: dao_uuid (address)
    // refUID: 0x0 (discarded, returns bytes32 attestation UID)
    string public constant PERMA_INSTANTIATE_SCHEMA =
        "uint8 protocol_version,string name,uint32 voting_period,uint32 voting_delay";

    // 3. GRANT
    // recipient: dao_uuid (address)
    // refUID: 0x0 (discarded, returns bytes32 attestation UID)
    // - verb: address being granted permissions
    // - permission: "GRANT", "CREATE_PROPOSAL_TYPE", "CREATE_PROPOSAL"
    // - level: 3-bit integer [UNDO, REVOKE, CREATE]
    // - filter: JSON string for granular control
    string public constant GRANT_SCHEMA =
        "address verb,string permission,uint8 level,string filter";

    // 4. CREATE_PROPOSAL_TYPE
    // recipient: dao_uuid (address)
    // refUID: 0x0 (returns bytes32 proposal_type_uid)
    // - class: must be "standard", "approval", "optimistic"
    // - kwargs: JSON with type-specific parameters
    string public constant CREATE_PROPOSAL_TYPE_SCHEMA =
        "string class,string kwargs";

    // 5. CREATE_PROPOSAL
    // recipient: dao_uuid (address)
    // refUID: proposal_type_uid or 0x0 if no type specified
    string public constant CREATE_PROPOSAL_SCHEMA =
        "uint256 proposal_id,string title,string description,uint64 startts,uint64 endts,string tags";

    // 6. SET_PROPOSAL_TYPE
    // recipient: dao_uuid (address)
    // refUID: proposal_type_uid
    string public constant SET_PROPOSAL_TYPE_SCHEMA =
        "uint256 proposal_id";

    // 7. SET_PARAM_VALUE
    // recipient: dao_uuid (address)
    // refUID: 0x0 (discarded, returns bytes32 attestation UID)
    // - param_name: name of the parameter to set
    // - param_value: uint256 value for the parameter
    string public constant SET_PARAM_VALUE_SCHEMA =
        "string param_name,uint256 param_value";

    // 8. SIMPLE_VOTE
    // recipient: dao_uuid (address)
    // refUID: 0x0 (discarded, returns bytes32 attestation UID)
    string public constant SIMPLE_VOTE_SCHEMA =
        "uint256 proposal_id,address voter,int8 choice,string reason";

    // 9. ADVANCED_VOTE
    // recipient: dao_uuid (address)
    // refUID: 0x0 (discarded, returns bytes32 attestation UID)
    string public constant ADVANCED_VOTE_SCHEMA =
        "uint256 proposal_id,address voter,string choice,string reason";

    // 10. UNDO
    // recipient: dao_uuid (address)
    // refUID: uid_of_attestation_to_undo
    string public constant UNDO_SCHEMA =
        "string verb";
}