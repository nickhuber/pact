var combatTrackerServices = angular.module('combatTrackerServices', ['ngResource']);

combatTrackerServices.factory('Character', ['$resource', function($resource) {
    return $resource('api/characters/:id', {id: '@id'});
}]);

combatTrackerServices.factory('Encounter', ['$resource', function($resource) {
    return $resource('api/encounters/:id', {id: '@id'})
}]);

combatTrackerServices.factory('EncounterCharacter', ['$resource', function($resource) {
    return $resource('api/encounter_characters/:id', {id: '@id'})
}]);
