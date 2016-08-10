var encounterServices = angular.module('encounterServices', ['ngResource']);


encounterServices.factory('Encounter', ['$resource', function($resource) {
    'use strict';
    return $resource(
        'api/encounters/:uuid/:action',
        {uuid: '@uuid'},
        {
            advance_initiative: {method: 'POST', params: {action: 'advance_initiative'}}
        }
    );
}]);


encounterServices.factory('EncounterCharacter', ['$resource', function($resource) {
    'use strict';
    return $resource(
        'api/encounter_characters/:uuid/',
        {uuid: '@uuid'},
        {
            update: {method: 'PATCH'}
        }
    );
}]);


encounterServices.factory('StatusEffect', ['$resource', function($resource) {
    'use strict';
    return $resource(
        'api/status_effects/:uuid/',
        {uuid: '@uuid'}
    );
}]);
