// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

import {UpgradableSchemaResolver} from "./UpgradableSchemaResolver.sol";
import {IEAS} from "eas-contracts/IEAS.sol";
import {Attestation} from "eas-contracts/Common.sol";

contract EntitiesResolver is UpgradableSchemaResolver {
    error InvalidAttester();

    event AttesterAdded(address indexed attester);
    event AttesterRemoved(address indexed attester);

    mapping(address => bool) public attesters;

    function initialize(
        IEAS eas,
        address _owner,
        address[] memory _attesters
    ) public initializer {
        UpgradableSchemaResolver.initialize(eas, _owner);

        for (uint256 i = 0; i < _attesters.length; i++) {
            attesters[_attesters[i]] = true;
            emit AttesterAdded(_attesters[i]);
        }
    }

    function addAttester(address _attester) public onlyOwner {
        attesters[_attester] = true;
        emit AttesterAdded(_attester);
    }

    function removeAttester(address _attester) public onlyOwner {
        attesters[_attester] = false;
        emit AttesterRemoved(_attester);
    }

    function onAttest(
        Attestation calldata attestation,
        uint256 /*value*/
    ) internal override returns (bool) {
        if (!attesters[attestation.attester]) {
            revert InvalidAttester();
        }

        return true;
    }

    function onRevoke(
        Attestation calldata /*attestation*/,
        uint256 /*value*/
    ) internal pure override returns (bool) {
        return true;
    }
}
