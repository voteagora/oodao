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
        address indexed voter,
        bytes32 indexed refUID,
        bytes data,
        bytes refData
    );

    mapping(bytes32 => mapping(address => bool)) internal _proposalVotes;

    function initialize(IEAS eas, address _owner) public override initializer {
        UpgradableSchemaResolver.initialize(eas, _owner);
    }

    function onAttest(
        Attestation calldata attestation,
        uint256 /*value*/
    ) internal override returns (bool) {
        address voter = attestation.attester;

        Attestation memory proposalAttestation = _eas.getAttestation(
            attestation.refUID
        );

        (, , uint64 startts, uint64 endts, ) = abi.decode(
            proposalAttestation.data,
            (string, string, uint64, uint64, string)
        );

        assert(proposalAttestation.recipient == attestation.recipient);

        if (block.timestamp < startts) {
            revert VotingNotStarted();
        }

        if (block.timestamp > endts) {
            revert VotingEnded();
        }

        if (_proposalVotes[attestation.refUID][voter]) {
            revert AlreadyVoted();
        }

        _countVote(voter, attestation.refUID);

        emit VoteCast(
            voter,
            attestation.refUID,
            attestation.data,
            proposalAttestation.data
        );

        return true;
    }

    function _countVote(address recipient, bytes32 proposalId) internal {
        _proposalVotes[proposalId][recipient] = true;
    }

    function onRevoke(
        Attestation calldata /*attestation*/,
        uint256 /*value*/
    ) internal pure override returns (bool) {
        return true;
    }
}
