var my_app = angular.module('myapp', ['ng.django.urls', 'ngGrid', 'ui.bootstrap'/* dependencies */]).config(function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
});

my_app.controller('RoomController', function($scope, $http, $window, djangoUrl, $location) {
    console.log("location = ", $location);
    $scope.currentLocation = $location.absUrl();
    console.log("outside of function, $location.absUrl() = ", $location.absUrl());
    console.log("outside of function, $scope.absUrl = ", $scope.currentLocation);
    $scope.allRooms = [];  
    var colDefs;  

    $scope.searchBet = [];
    $scope.dt1 = new Date();    
    $scope.dt2 = new Date();

    $scope.format = 'dd-MMMM-yyyy';
    $scope.open = function($event, opened) {
        $event.preventDefault();
        $event.stopPropagation();

        $scope[opened] = true;
    };

    $scope.gridOptions = { data: 'allRooms',
                            showFilter : true,
                            enableColumnResize : true,
                            // columnDefs : colDefs
                           columnDefs:[
                            {field:'title', displayName: 'Bet Title'},
                            {field:'challenged_bet', displayName: "Challenged Bet"},
                            {field:'challenged_name', displayName: "Challenged Name"}, 
                            {field:'date_created', displayName: "Date Created"}
                            // {field:'room_key', displayName: "Room Key"} 
                           ]
                       };


    $scope.submit = function() {
        var in_data = angular.toJson($scope.room_data);
        console.log($scope);
        $http.post(djangoUrl.reverse('room-list'), in_data)
            .success(function(out_data) {
                console.log("Success");
                console.log(out_data);
                $window.location.href = djangoUrl.reverse('thanks');
            });
    }

    $scope.getKeyFromUrl = function(){
        console.log('current $location.absUrl = ', $scope.currentLocation);
        console.log('inside function, $location = ', $location);
        $http({ //toldyouso.com/room/rooms/1?title=abc
            url: $location.absUrl, //toldyouso.com/room/rooms/1
            method: "GET",
            params: {title: $location.search()} //CONTINUE HERE! Not sure what to put here!abc
        })
        .success(function (data){
            console.log(data);
            console.log(djangoUrl.reverse('room-list'));
            $scope.allRooms = data.results; 
            console.log('$scope.allRooms = ', $scope.allRooms);
    });
    }


    $scope.getAllRooms = function(){
        $http.get(djangoUrl.reverse('room-list'))
            .success(function (data){
                console.log(data);
                $scope.allRooms = data.results; 
                // colDefs = makeColDefs(data.results[0]);
                // colDefs = autoColWidth(colDefs, data.results[0]);
 
                console.log('$scope.allRooms = ', $scope.allRooms);
                console.log('$scope = ', $scope);
            })
    }

});

