// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

import {ISchemaResolver} from "eas-contracts/resolver/ISchemaResolver.sol";
import {IEAS} from "eas-contracts/IEAS.sol";
import {Attestation, InvalidLength, AccessDenied, uncheckedInc} from "eas-contracts/Common.sol";
import {InvalidEAS} from "eas-contracts/Common.sol";
import {OwnableUpgradeable} from "@openzeppelin/contracts-upgradeable/access/OwnableUpgradeable.sol";

abstract contract UpgradableSchemaResolver is
    OwnableUpgradeable,
    ISchemaResolver
{
    error InsufficientValue();
    error NotPayable();

    // Resolver contract version. Compatible with Semver.
    string internal constant SEMVER = "1.3.0";

    // The global EAS contract.
    IEAS internal _eas;

    /// @dev Disable constructor.
    constructor() {
        _disableInitializers();
    }

    /// @dev Ensures that only the EAS contract can make this call.
    modifier onlyEAS() {
        _onlyEAS();

        _;
    }

    /// @dev Initializes the resolver implementation.
    /// @param eas The address of the global EAS contract.
    function initialize(IEAS eas, address _owner) public virtual initializer {
        __SchemaResolver_init(eas);
        __Ownable_init(_owner);
    }

    /// @dev Re-initializes the `SchemaResolver` contract (internal).
    function __SchemaResolver_init(IEAS eas) internal initializer {
        if (address(eas) == address(0)) {
            revert InvalidEAS();
        }

        _eas = eas;
    }

    /// @inheritdoc ISchemaResolver
    function isPayable() public pure virtual returns (bool) {
        return false;
    }

    /// @dev ETH callback.
    receive() external payable virtual {
        if (!isPayable()) {
            revert NotPayable();
        }
    }

    /// @inheritdoc ISchemaResolver
    function attest(
        Attestation calldata attestation
    ) external payable onlyEAS returns (bool) {
        return onAttest(attestation, msg.value);
    }

    /// @inheritdoc ISchemaResolver
    function multiAttest(
        Attestation[] calldata attestations,
        uint256[] calldata values
    ) external payable onlyEAS returns (bool) {
        uint256 length = attestations.length;
        if (length != values.length) {
            revert InvalidLength();
        }

        // We are keeping track of the remaining ETH amount that can be sent to resolvers and will keep deducting
        // from it to verify that there isn't any attempt to send too much ETH to resolvers. Please note that unless
        // some ETH was stuck in the contract by accident (which shouldn't happen in normal conditions), it won't be
        // possible to send too much ETH anyway.
        uint256 remainingValue = msg.value;

        for (uint256 i = 0; i < length; i = uncheckedInc(i)) {
            // Ensure that the attester/revoker doesn't try to spend more than available.
            uint256 value = values[i];
            if (value > remainingValue) {
                revert InsufficientValue();
            }

            // Forward the attestation to the underlying resolver and return false in case it isn't approved.
            if (!onAttest(attestations[i], value)) {
                return false;
            }

            unchecked {
                // Subtract the ETH amount, that was provided to this attestation, from the global remaining ETH amount.
                remainingValue -= value;
            }
        }

        return true;
    }

    /// @inheritdoc ISchemaResolver
    function revoke(
        Attestation calldata attestation
    ) external payable onlyEAS returns (bool) {
        return onRevoke(attestation, msg.value);
    }

    /// @inheritdoc ISchemaResolver
    function multiRevoke(
        Attestation[] calldata attestations,
        uint256[] calldata values
    ) external payable onlyEAS returns (bool) {
        uint256 length = attestations.length;
        if (length != values.length) {
            revert InvalidLength();
        }

        // We are keeping track of the remaining ETH amount that can be sent to resolvers and will keep deducting
        // from it to verify that there isn't any attempt to send too much ETH to resolvers. Please note that unless
        // some ETH was stuck in the contract by accident (which shouldn't happen in normal conditions), it won't be
        // possible to send too much ETH anyway.
        uint256 remainingValue = msg.value;

        for (uint256 i = 0; i < length; i = uncheckedInc(i)) {
            // Ensure that the attester/revoker doesn't try to spend more than available.
            uint256 value = values[i];
            if (value > remainingValue) {
                revert InsufficientValue();
            }

            // Forward the revocation to the underlying resolver and return false in case it isn't approved.
            if (!onRevoke(attestations[i], value)) {
                return false;
            }

            unchecked {
                // Subtract the ETH amount, that was provided to this attestation, from the global remaining ETH amount.
                remainingValue -= value;
            }
        }

        return true;
    }

    /// @notice A resolver callback that should be implemented by child contracts.
    /// @param attestation The new attestation.
    /// @param value An explicit ETH amount that was sent to the resolver. Please note that this value is verified in
    ///     both attest() and multiAttest() callbacks EAS-only callbacks and that in case of multi attestations, it'll
    ///     usually hold that msg.value != value, since msg.value aggregated the sent ETH amounts for all the
    ///     attestations in the batch.
    /// @return Whether the attestation is valid.
    function onAttest(
        Attestation calldata attestation,
        uint256 value
    ) internal virtual returns (bool);

    /// @notice Processes an attestation revocation and verifies if it can be revoked.
    /// @param attestation The existing attestation to be revoked.
    /// @param value An explicit ETH amount that was sent to the resolver. Please note that this value is verified in
    ///     both revoke() and multiRevoke() callbacks EAS-only callbacks and that in case of multi attestations, it'll
    ///     usually hold that msg.value != value, since msg.value aggregated the sent ETH amounts for all the
    ///     attestations in the batch.
    /// @return Whether the attestation can be revoked.
    function onRevoke(
        Attestation calldata attestation,
        uint256 value
    ) internal virtual returns (bool);

    /// @dev Ensures that only the EAS contract can make this call.
    function _onlyEAS() private view {
        if (msg.sender != address(_eas)) {
            revert AccessDenied();
        }
    }

    /// @dev Version
    function version() external pure override returns (string memory) {
        return SEMVER;
    }
}
