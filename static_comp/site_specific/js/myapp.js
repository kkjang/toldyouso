var my_app = angular.module('myapp', ['ng.django.urls', 'ngGrid', 'ui.bootstrap'/* dependencies */]).config(function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
});

my_app.controller('RoomController', function($scope, $http, $window, djangoUrl, $location) {
    // console.log("location = ", $location);
    $scope.currentLocation = $location.absUrl();
    // console.log("outside of function, $location.absUrl() = ", $location.absUrl());
    // console.log("outside of function, $scope.absUrl = ", $scope.currentLocation);
    $scope.allBets = [];  
    $scope.processedBets = [];
    $scope.processedBet = [];
    // $scope.processedBet = [{
    //     betTitle: "",
    //     challengerName: "",
    //     challengerAmount: "",
    //     challengerCondition: "",
    //     challengedName: "",
    //     challengedAmount: "",
    //     challengedCondition:  ""
    // }];



    //CODE RELATED TO SELECTING THE FILTER
    $scope.betFilterOptions = { title: "Bet Title",
                                challengerCondition: "Challenger Condition",
                                challengerAmount: "Challenger Amount",
                                challengedCondition: "Challenged Condition",
                                challengedAmount: "Challenged Amount", 
                                dateCreated: "Date Created", 
                                dateAccepted: "Date Accepted"};

    // $scope.selectedFilter
    $scope.titleSelected = true; 
    $scope.challengerConditionSelected = false; 
    $scope.challengerAmountSelected = false; 
    $scope.challengedConditionSelected = false;
    $scope.challengedAmountSelected = false;
    $scope.dateCreatedSelected = false;
    $scope.dateAcceptedSelected = false; 

    $scope.$watch('betFilterOptions', function(newValue, oldValue) {
        console.log("betFilterOptions oldValue = ", oldValue);
        console.log("betFilterOptions newValue = ", newValue);
    });

    $scope.searchBet = {title: "",
                        challengedBet: "",
                        challengedName: "", 
                        startDate: "",
                        endDate: ""
                        };

    // $scope.$watch('searchBet', function(newValue, oldValue) {
    //     console.log("searchBet oldValue = ", oldValue);
    //     console.log("searchBet newValue = ", newValue);
    // });

    $scope.updateOptionsView = function(selectedFilter){
        if(selectedFilter === $scope.betFilterOptions.title){
            $scope.titleSelected = true; 
            $scope.challengerConditionSelected = false; 
            $scope.challengerAmountSelected = false; 
            $scope.challengedConditionSelected = false;
            $scope.challengedAmountSelected = false;
            $scope.dateCreatedSelected = false;
            $scope.dateAcceptedSelected = false; 
        }
        else if(selectedFilter === $scope.betFilterOptions.challengerCondition){
            $scope.titleSelected = false; 
            $scope.challengerConditionSelected = true; 
            $scope.challengerAmountSelected = false; 
            $scope.challengedConditionSelected = false;
            $scope.challengedAmountSelected = false;
            $scope.dateCreatedSelected = false;
            $scope.dateAcceptedSelected = false; 
        }
        

    }

    $scope.dt1 = new Date();    
    $scope.dt2 = new Date();

    $scope.format = 'dd-MMMM-yyyy';
    
    $scope.open = function($event, opened) {
        $event.preventDefault();
        $event.stopPropagation();
        $scope[opened] = true;
    };

    $scope.status = {
        isopen: false
    };
    //SETTING UP THE ROOMS TABLE 
    $scope.gridOptions = { data: 'processedBets',
                            showFilter : true,
                            enableColumnResize : true,
                            columnDefs:[
                            {field:'betTitle', displayName: 'Bet Title'},
                            {field:'challengerCondition', displayName: "Challenger Condition"},
                            {field:'challengerAmount', displayName: "Challenger Amount"},
                            {field:'challengedCondition', displayName: "Challenged Condition"}, 
                            {field:'challengedAmount', displayName: "Challenged Amount"},
                            {field:'dateCreated', displayName: "Date Created"}
                           ]
                       };

    $scope.submit = function() {
        var in_data = angular.toJson($scope.bet_data);
        $http.post(djangoUrl.reverse('bet-list'), in_data)
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
            $scope.theBetKey = data.results; 
    });
    }


    $scope.getAllBets = function(){
        $http.get(djangoUrl.reverse('bet-list'))
            .success(function (data){
                $scope.allBets = data.results;
                // console.log('$scope.allBets = ', $scope.allBets);
                var i = 0;
                var j = 0;
                for(i = 0; i <$scope.allBets.length; i++){
                    $scope.processedBet = [];
                    $scope.processedBet.betTitle = $scope.allBets[i].title;
                    $scope.processedBet.dateCreated = $scope.allBets[i].date_created;
                    if($scope.allBets[i].wagers[0].user_id === $scope.allBets[i].creator_id){
                        // $scope.processedBet.challengerName = $scope.allBets[i].wagers[0].user_name;
                        // $scope.processedBet.challengedName = $scope.allBets[i].wagers[1].user_name;
                        $scope.processedBet.challengerCondition = $scope.allBets[i].wagers[0].condition;
                        $scope.processedBet.challengerAmount = $scope.allBets[i].wagers[0].amount;
                        $scope.processedBet.challengedCondition = $scope.allBets[i].wagers[1].condition;
                        $scope.processedBet.challengedAmount = $scope.allBets[i].wagers[1].amount;

                    }
                    else if ($scope.allBets[i].wagers[1].user_id === $scope.allBets[i].creator_id){
                        // $scope.processedBet.challengerName = $scope.allBets[i].wagers[1].user_name
                        // $scope.processedBet.challengedName = $scope.allBets[i].wagers[0].user_name;
                        $scope.processedBet.challengerAmount = $scope.allBets[i].wagers[1].amount;
                        $scope.processedBet.challengerCondition = $scope.allBets[i].wagers[1].condition; 
                        $scope.processedBet.challengedCondition = $scope.allBets[i].wagers[0].condition;
                        $scope.processedBet.challengedAmount = $scope.allBets[i].wagers[0].amount;
                    }
                    // console.log("$scope.processedBet = ", $scope.processedBet); 
                    $scope.processedBets.push($scope.processedBet);  
                }
                // console.log("$scope.processedBets = ", $scope.processedBets);
            });
    }

});

