var encounterControllers = angular.module('encounterControllers', ['xeditable', 'ui.bootstrap']);


encounterControllers.run(function(editableOptions) {
    editableOptions.theme = 'bs3';
});


encounterControllers.controller('CharacterCreateCtrl', function ($scope, $location, Character) {
    $scope.character = new Character();
    $scope.errors = {};

    $scope.create = function() {
        $scope.character.$save().then(function(newCharacter) {
            $location.path('/characters/' + newCharacter.id);
        }).catch(function(errorResponse) {
            $scope.errors = errorResponse.data;
        });
    };
});


encounterControllers.controller('EncounterListCtrl', function($scope, encounters) {
    $scope.encounters = encounters;
});


encounterControllers.controller('EncounterDetailCtrl', function ($scope, $location, $uibModal, EncounterCharacter, encounter, characters) {
    $scope.encounter = encounter;
    $scope.characters = characters;

    $scope.newCharacter = {};

    $scope.end = function() {
        $scope.encounter.$delete().then(function() {
            $location.path('/encounters/');
        });
    };

    $scope.advanceInit = function() {
        $scope.encounter.$advance_initiative();
    };

    $scope.addCharacter = function() {
        var ec = new EncounterCharacter();
        ec.encounter = $scope.encounter.url;
        ec.character = $scope.newCharacter.url;
        ec.initiative = $scope.newCharacter.initiative;
        ec.notes = $scope.newCharacter.notes;
        ec.$save().then(function(newEncounterCharacter) {
            $scope.encounter.characters.push(newEncounterCharacter);
        }).catch(function(errorResponse) {
            $scope.errors = errorResponse.data;
        });
    };

    $scope.removeCharacter = function(character) {
        EncounterCharacter.delete({id: character.id});
        $scope.encounter.characters = _.without($scope.encounter.characters, character);
    };

    $scope.updateCharacter = function(character) {
        EncounterCharacter.update({id: character.id}, character);
    };

    $scope.increaseInitiative = function(character) {
        character.initiative += 1;
        EncounterCharacter.update({id: character.id}, {initiative: character.initiative});
    };

    $scope.decreaseInitiative = function(character) {
        character.initiative -= 1;
        EncounterCharacter.update({id: character.id}, {initiative: character.initiative});
    };

    $scope.hurtCharacter = function(character) {
        if (!_.isNumber(character.hp_change_value)) {
            return;
        }
        character.current_hp -= character.hp_change_value;
        EncounterCharacter.update({id: character.id}, {current_hp: character.current_hp});
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
        EncounterCharacter.update({id: character.id}, {current_hp: character.current_hp});
        character.hp_change_value = null;
    };

    $scope.showCharacter = function(character) {
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
});


encounterControllers.controller('CharacterInfoModalCtrl', function ($scope, $uibModalInstance, character) {
    $scope.character = character;

    $scope.ok = function () {
        $uibModalInstance.close();
    };
});


encounterControllers.controller('EncounterCreateCtrl', function ($scope, $location, Encounter) {
    $scope.encounter = new Encounter();
    $scope.errors = {};

    $scope.create = function() {
        $scope.encounter.$save().then(function(newEncounter) {
            $location.path('/encounters/' + newEncounter.id);
        }).catch(function(errorResponse) {
            $scope.errors = errorResponse.data;
        });
    };
});
