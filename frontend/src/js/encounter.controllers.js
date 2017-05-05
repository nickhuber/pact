(function() {
    'use strict';
    var encounterControllers = angular.module('encounterControllers', ['xeditable', 'ui.bootstrap', 'hc.marked']);


    encounterControllers.run(function(editableOptions) {
        editableOptions.theme = 'bs3';
    });


    encounterControllers.controller('EncounterListCtrl', function($scope, encounters) {
        $scope.encounters = encounters;
    });


    encounterControllers.controller('EncounterDetailCtrl', function ($scope, $q, $location, $uibModal, Encounter, EncounterCharacter, StatusEffect, encounter, players, npcs) {
        $scope.encounter = encounter;
        $scope.players = players;
        $scope.npcs = npcs;

        $scope.addPlayer = false;
        $scope.addNPC = false;

        $scope.newCharacterErrors = {};
        $scope.newCharacter = {
            quantity: 1
        };

        $scope.updateEncounter = function() {
            $scope.encounter.$update().then(function(response) {
                $scope.errors = {};
            }).catch(function(response) {
                $scope.errors = response.data;
            });
        };

        $scope.resetNewCharacter = function() {
            $scope.addPlayer = false;
            $scope.addNPC = false;

            $scope.newCharacterErrors = {};
            $scope.newCharacter = {
                quantity: 1
            };
        };

        $scope.addNewPlayerCharacter = function() {
            $scope.addPlayer = true;
            $scope.newCharacter.url = players[0].url;
        };

        $scope.addNewNonPlayerCharacter = function() {
            $scope.addNPC = true;
            $scope.newCharacter.url = npcs[0].url;
        };

        $scope.cancelAddCharacter = function() {
            $scope.resetNewCharacter();
        };

        $scope.end = function() {
            $scope.encounter.$delete().then(function() {
                $location.path('/encounters/');
            });
        };

        $scope.advanceInit = function() {
            $scope.encounter.$advance_initiative();
        };

        $scope.isActiveCharacter = function(character) {
            return _.contains($scope.encounter.active_character_uuids, character.uuid);
        }

        $scope.addCharacter = function() {
            var promises = [];
            function handleSuccess(newEncounterCharacter) {
                $scope.encounter.characters.push(newEncounterCharacter);
                // Refresh the encounter object
                Encounter.get($scope.encounter.uuid).then(function(encounter) {
                    $scope.encounter = encounter;
                });
            }
            function handleError(errorResponse) {
                $scope.newCharacterErrors = errorResponse.data;
            }
            for (var i = 0; i < $scope.newCharacter.quantity; i++) {
                var ec = new EncounterCharacter();
                ec.encounter = $scope.encounter.url;
                ec.character = $scope.newCharacter.url;
                ec.initiative = $scope.newCharacter.initiative;
                ec.notes = $scope.newCharacter.notes;
                promises.push(
                    ec.$save().then(handleSuccess).catch(handleError)
                );
            }
            $q.all(promises).finally(function() {
                $scope.resetNewCharacter();
            });
        };

        $scope.addToInitiative = function(character) {
            if (!_.isNumber(character._initiative)) {
                // TODO: show an error here, or use a form and submit properly.
                return;
            }
            character.initiative = character._initiative;
            delete character._initiative;
            EncounterCharacter.update(character, character);
        };

        $scope.pendingCharacters = function() {
            return _.filter($scope.encounter.characters, function(character) {
                return character.initiative === null;
            });
        };

        $scope.charactersInInitiative = function() {
            return _.filter($scope.encounter.characters, function(character) {
                return character.initiative !== null;
            });
        };

        $scope.removeCharacter = function(character) {
            EncounterCharacter.delete(character);
            $scope.encounter.characters = _.without($scope.encounter.characters, character);
        };

        $scope.updateCharacter = function(character) {
            EncounterCharacter.update(character, character);
        };

        $scope.increaseInitiative = function(character) {
            character.initiative += 1;
            EncounterCharacter.update(character, {initiative: character.initiative});
        };

        $scope.decreaseInitiative = function(character) {
            character.initiative -= 1;
            EncounterCharacter.update(character, {initiative: character.initiative});
        };

        $scope.hurtCharacter = function(character) {
            if (!_.isNumber(character.hp_change_value)) {
                return;
            }
            character.current_hp -= character.hp_change_value;
            EncounterCharacter.update(character, {current_hp: character.current_hp});
            character.hp_change_value = null;
        };

        $scope.healCharacter = function(character) {
            if (!_.isNumber(character.hp_change_value)) {
                return;
            }
            character.current_hp += character.hp_change_value;
            if (character.current_hp > character.max_hp) {
                character.current_hp = character.max_hp;
            }
            EncounterCharacter.update(character, {current_hp: character.current_hp});
            character.hp_change_value = null;
        };

        $scope.showCharacterModal = function(character) {
            $uibModal.open({
                templateUrl: 'characterDetailsModal.html',
                controller: 'CharacterInfoModalCtrl',
                size: 'lg',
                resolve: {
                    character: function () {
                        return character;
                    }
                }
            });
        };

        $scope.showAddStatusModal = function(character) {
            var status_effect = new StatusEffect();
            status_effect.character = character.url;
            var modalInstance = $uibModal.open({
                templateUrl: 'addStatusEffect.html',
                controller: 'addStatusEffectModalCtrl',
                size: 'lg',
                resolve: {
                    status_effect: function () {
                        return status_effect;
                    },
                    character: function () {
                        return character;
                    }
                }
            });
            modalInstance.result.then(function(newStatusEffect) {
                character.status_effects.push(newStatusEffect);
            });
        };

        $scope.removeStatus = function(character, status) {
            StatusEffect.delete(status);
            character.status_effects = _.without(character.status_effects, status);
        };

    });


    encounterControllers.controller('CharacterInfoModalCtrl', function ($scope, $uibModalInstance, character) {
        $scope.character = character;

        $scope.ok = function () {
            $uibModalInstance.close();
        };
    });


    encounterControllers.controller('addStatusEffectModalCtrl', function ($scope, $uibModalInstance, status_effect, character) {
        $scope.status_effect = status_effect;
        $scope.character = character;
        $scope.errors = {};

        $scope.add = function () {
            status_effect.$save().then(function(newStatusEffect) {
                $uibModalInstance.close(newStatusEffect);
            }).catch(function(errorResponse) {
                $scope.errors = errorResponse.data;
            });
        };

        $scope.cancel = function () {
            $uibModalInstance.dismiss();
        };
    });


    encounterControllers.controller('EncounterCreateCtrl', function ($scope, $location, Encounter) {
        $scope.encounter = new Encounter();
        $scope.errors = {};

        $scope.create = function() {
            $scope.encounter.$save().then(function(newEncounter) {
                $location.path('/encounters/' + newEncounter.uuid);
            }).catch(function(errorResponse) {
                $scope.errors = errorResponse.data;
            });
        };
    });
})();
