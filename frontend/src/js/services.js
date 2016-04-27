var combatTrackerServices = angular.module('combatTrackerServices', ['ngResource']);


combatTrackerServices.factory('Character', ['$resource', function($resource) {
    return $resource(
        'api/characters/:id',
        {id: '@id'}
    );
}]);


combatTrackerServices.factory('Encounter', ['$resource', function($resource) {
    return $resource(
        'api/encounters/:id/:action',
        {id: '@id'}, 
        {
            advance_initiative: {method: 'POST', params: {action: 'advance_initiative'}}
        }
    );
}]);


combatTrackerServices.factory('EncounterCharacter', ['$resource', function($resource) {
    return $resource(
        'api/encounter_characters/:id/',
        {id: '@id'},
        {
            update: {method: 'PATCH'}
        }
    );
}]);
