var encounterServices = angular.module('encounterServices', ['ngResource']);


encounterServices.factory('Encounter', ['$resource', function($resource) {
    return $resource(
        'api/encounters/:id/:action',
        {id: '@id'},
        {
            advance_initiative: {method: 'POST', params: {action: 'advance_initiative'}}
        }
    );
}]);


encounterServices.factory('EncounterCharacter', ['$resource', function($resource) {
    return $resource(
        'api/encounter_characters/:id/',
        {id: '@id'},
        {
            update: {method: 'PATCH'}
        }
    );
}]);
