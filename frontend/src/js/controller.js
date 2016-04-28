var combatTrackerControllers = angular.module('combatTrackerControllers', ['xeditable']);


combatTrackerControllers.run(function(editableOptions) {
  editableOptions.theme = 'bs3';
});


combatTrackerControllers.controller('CharacterListCtrl', ['$scope', 'Character',
    function ($scope, Character) {
        $scope.characters = Character.query();
    }
]);


combatTrackerControllers.controller('CharacterDetailCtrl', ['$scope', '$location', '$routeParams', 'Character',
    function ($scope, $location, $routeParams, Character) {
        $scope.character = Character.get($routeParams);

        $scope.delete = function() {
            $scope.character.$delete().then(function() {
                $location.path('/characters/');
            }).catch(function(response) {
                // TODO: show delete error
            });
        };
    }
]);


combatTrackerControllers.controller('CharacterCreateCtrl', ['$scope', '$location', 'Character',
    function ($scope, $location, Character) {
        $scope.character = new Character();
        $scope.errors = {};

        $scope.create = function() {
            $scope.character.$save().then(function(newCharacter) {
                $location.path('/characters/' + newCharacter.id);
            }).catch(function(errorResponse) {
                $scope.errors = errorResponse.data;
            });
        };
    }
]);


combatTrackerControllers.controller('EncounterListCtrl', ['$scope', 'Encounter',
    function($scope, Encounter) {
        $scope.encounters = Encounter.query();
    }
]);


combatTrackerControllers.controller('EncounterDetailCtrl', ['$scope', '$location', '$routeParams', 'Encounter', 'Character', 'EncounterCharacter',
    function ($scope, $location, $routeParams, Encounter, Character, EncounterCharacter) {
        $scope.encounter = Encounter.get($routeParams);
        $scope.characters = Character.query();
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
            EncounterCharacter.update({id: character.id}, {initiative: character.initiative + 1});
            character.initiative += 1;
        };

        $scope.decreaseInitiative = function(character) {
            EncounterCharacter.update({id: character.id}, {initiative: character.initiative - 1});
            character.initiative -= 1;
        };
    }
]);


combatTrackerControllers.controller('EncounterCreateCtrl', ['$scope', '$location', 'Encounter',
    function ($scope, $location, Encounter) {
        $scope.encounter = new Encounter();
        $scope.errors = {};

        $scope.create = function() {
            $scope.encounter.$save().then(function(newEncounter) {
                $location.path('/encounters/' + newEncounter.id);
            }).catch(function(errorResponse) {
                $scope.errors = errorResponse.data;
            });
        };
    }
]);


combatTrackerControllers.controller('NavigationCtrl', ['$scope', '$http', '$location',
    function ($scope, $http, $location)  {
        $scope.rollQuery = '';
        $scope.rollResult = '';

        $scope.isActive = function (viewLocation) {
            return $location.$$path === viewLocation;
        };

        $scope.rollDice = function() {
            $http.post(
                '/api/roll',
                {query: $scope.rollQuery}
            )
            .then(function(response) {
                $scope.rollResult = response.data.total;
            });
        };
    }
]);
