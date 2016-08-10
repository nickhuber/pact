var directives = angular.module('directives', ['ui.bootstrap']);

directives.directive('nhConfirmClick', function($uibModal) {
    'use strict';
    return {
        priority: -1,
        restrict: 'A',
        scope: { nhConfirmFunction: '&nhConfirmClick' },
        link: function(scope, element, attrs) {
            element.bind('click', function(e) {
                var message = attrs.nhConfirmClickMessage ? attrs.nhConfirmClickMessage : 'Are you sure?';
                $uibModal.open({
                    templateUrl: 'templates/confirm-click-modal.html',
                    controller: 'ConfirmClickModalCtrl',
                    size: 'lg',
                    resolve: {
                        confirmFunction: function () {
                            return scope.nhConfirmFunction;
                        },
                        message: function() {
                            return message;
                        }
                    }
                });
            });
        }
    };
});

directives.controller('ConfirmClickModalCtrl', function ($scope, $uibModalInstance, confirmFunction, message) {
    'use strict';
    $scope.message = message;

    $scope.yes = function () {
        confirmFunction();
        $uibModalInstance.close();
    };

    $scope.no = function () {
        $uibModalInstance.dismiss();
    };
});
