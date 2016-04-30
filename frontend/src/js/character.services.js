var characterServices = angular.module('characterServices', ['ngResource']);

characterServices.factory('Character', ['$resource', function($resource) {
    return $resource(
        'api/characters/:id',
        {id: '@id'},
        {
            update: {method: 'PATCH'}
        }
    );
}]);
