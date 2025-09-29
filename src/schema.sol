// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/// @title DaoSchemas v0.1.0
/// @notice Schema definitions for the EAS-Based DAO Protocol v0.1.0
/// @dev These schema strings should be registered on EAS SchemaRegistry.

contract DaoSchemasV010 {
    // 1. INSTANTIATE
    string public constant INSTANTIATE_SCHEMA =
        "bytes32 dao_uuid,string protocol_version,string name";

    // 2. GRANT
    // - permission: "GRANT", "CREATE_PROPOSAL_TYPE", "CREATE_PROPOSAL"
    // - level: 3-bit integer [UNDO, REVOKE, CREATE]
    // - filter: JSON string for granular control
    string public constant GRANT_SCHEMA =
        "bytes32 dao_uuid,address subject,string permission,uint8 level,string filter";

    // 3. CREATE_PROPOSAL_TYPE
    // - class: must be "standard", "approval", "optimistic"
    // - kwargs: JSON with type-specific parameters
    string public constant CREATE_PROPOSAL_TYPE_SCHEMA =
        "bytes32 dao_uuid,bytes32 proposal_type_uuid,string class,string kwargs";

    // 4. CREATE_PROPOSAL
    string public constant CREATE_PROPOSAL_SCHEMA =
        "bytes32 dao_uuid,bytes32 proposal_uuid,bytes32 proposal_type_uuid,"
        "string title,string description,uint64 startts,uint64 endts";

    // 5a. SIMPLE_VOTE
    string public constant SIMPLE_VOTE_SCHEMA =
        "bytes32 dao_uuid,bytes32 proposal_uuid,address voter,"
        "int8 choice,string reason,uint256 weight";

    // 5b. ADVANCED_VOTE
    string public constant ADVANCED_VOTE_SCHEMA =
        "bytes32 dao_uuid,bytes32 proposal_uuid,address voter,"
        "string choice,string reason,uint256 weight";

    // 6. UNDO
    string public constant UNDO_SCHEMA =
        "bytes32 dao_uuid,bytes32 uid";
}