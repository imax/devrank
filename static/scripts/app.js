(function () {
    'use strict';


    function configure($stateProvider, $urlRouterProvider) {
        $urlRouterProvider.otherwise(function ($injector) {
            var $state = $injector.get('$state');
            $state.go('base');
        });

        $stateProvider
            .state('base', {
                url: '/',
                templateUrl: 'static/views/base.html'
            });

    }

    angular.module('devrankApp', [
            'ui.router',
            'gettext',
        ])
        .config(configure).controller('FilterCtrl', function ($scope, $http) {

            $scope.init = function () {
                var url = 'http://127.0.0.1:5000/init';
                $http({
                    method: 'GET',
                    url: url,
                }).success(
                    function (data, status, headers, config) {
                        $scope.langs = data['job_title'];
                    }
                ).error(
                    function (data, status, headers, config) {
                        $scope.langs = '';
                    }
                );
            }

            $scope.search = function() {
                var url = 'http://127.0.0.1:5000/search';
                $http({
                    method: 'GET',
                    params: { special: $('#special').val(), 
                            salary: $('#salary').val()},
                    url: url,
                }).success(
                    function (data, status, headers, config) {
                        $scope.stats_popular = data['stats_popular'];
                        $scope.stats_top = data['stats_top'];
                        $scope.stats_candidate_deals = data['stats_candidate_deals'];
                    }
                ).error(
                    function (data, status, headers, config) {
                        $scope.langs = '';
                    }
                );
            }

        });
})();