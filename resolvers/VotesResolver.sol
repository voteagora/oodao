// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

import {UpgradableSchemaResolver} from "./UpgradableSchemaResolver.sol";
import {IEAS} from "eas-contracts/IEAS.sol";
import {Attestation} from "eas-contracts/Common.sol";

contract VotesResolver is UpgradableSchemaResolver {
    error InvalidAttester();
    error AlreadyVoted();
    error VotingNotStarted();
    error VotingEnded();

    event VoteCast(
        uint256 indexed proposalId,
        address indexed voter,
        bytes32 indexed refUID,
        bytes data,
        bytes refData
    );

    bytes32 public VOTER_SCHEMA_UID;

    mapping(uint256 => mapping(address => bool)) internal _proposalVotes;

    function initialize(
        IEAS eas,
        address _owner,
        bytes32 _voterSchemaUID
    ) public initializer {
        UpgradableSchemaResolver.initialize(eas, _owner);
        VOTER_SCHEMA_UID = _voterSchemaUID;
    }

    function onAttest(
        Attestation calldata attestation,
        uint256 /*value*/
    ) internal override returns (bool) {
        (uint256 proposalId, , ) = abi.decode(
            attestation.data,
            (uint256, int8, string)
        );

        address voter = attestation.attester;

        Attestation memory proposalAttestation = _eas.getAttestation(
            attestation.refUID
        );

        (, , , uint64 startts, uint64 endts, ) = abi.decode(
            proposalAttestation.data,
            (uint256, string, string, uint64, uint64, string)
        );

        if (block.timestamp < startts) {
            revert VotingNotStarted();
        }

        if (block.timestamp > endts) {
            revert VotingEnded();
        }

        if (_proposalVotes[proposalId][voter]) {
            revert AlreadyVoted();
        }

        _countVote(voter, proposalId);

        emit VoteCast(
            proposalId,
            voter,
            attestation.refUID,
            attestation.data,
            proposalAttestation.data
        );

        return true;
    }

    function _countVote(address recipient, uint256 proposalId) internal {
        _proposalVotes[proposalId][recipient] = true;
    }

    function onRevoke(
        Attestation calldata /*attestation*/,
        uint256 /*value*/
    ) internal pure override returns (bool) {
        return true;
    }
}
