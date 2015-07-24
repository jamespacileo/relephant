(function() {
  var app;

  app = angular.module("DragonDemoApp", ['SwampDragonServices']);

  app.controller("GameCommentsCtrl", function($scope, $dragon) {
    $scope.todoList = {};
    $scope.todoItems = [];
    $scope.channel = 'global';
    $scope.playerNumber = Math.floor(Math.random() * 500);
    $scope.playerName = "player" + $scope.playerNumber;
    $scope.comments = [];
    $scope.$watch("comments", function() {
      return $(".comments").scrollTop = $(".comments");
    });
    $scope.commentForm = {
      text: "",
      command: null
    };
    RPGJS.defines({
      canvas: "game-canvas"
    }).ready(function() {
      return RPGJS.Scene.map();
    });
    $("body").on("keydown", "textarea", function(event) {
      event.stopPropagation();
      return console.log("KEYDOWN!");
    });
    $scope.$watch("commentForm.text", function(newVal) {
      if (!newVal) {
        $scope.commentForm.command = null;
        return;
      }
      if (newVal.toLowerCase().indexOf("up") >= 0) {
        $scope.commentForm.command = "up";
        return;
      }
      if (newVal.toLowerCase().indexOf("down") >= 0) {
        $scope.commentForm.command = "down";
        return;
      }
      if (newVal.toLowerCase().indexOf("left") >= 0) {
        $scope.commentForm.command = "left";
        return;
      }
      if (newVal.toLowerCase().indexOf("right") >= 0) {
        $scope.commentForm.command = "right";
        return;
      }
      return $scope.commentForm.command = null;
    });
    swampdragon.ready(function() {
      console.log("ready");
      swampdragon.subscribe('game', $scope.channel, null, function(context, data) {
        console.log("subscribe", context, data);
        this.dataMapper = new DataMapper(data);
      });
      return swampdragon.onChannelMessage(function(channels, message) {
        var i, new_pos;
        console.log("onChannelMessage", channels, message);
        if (message.data.type === "comment") {
          $scope.comments.push(message.data);
          $scope.$apply();
        }
        if (message.data.type === "move") {
          new_pos = message.data.position;
          if (message.data.direction === "bottom") {
            new_pos[1] -= 1;
          }
          if (message.data.direction === "top") {
            new_pos[1] += 1;
          }
          if (message.data.direction === "left") {
            new_pos[0] += 1;
          }
          if (message.data.direction === "right") {
            new_pos[0] -= 1;
          }
          RPGJS.Player.moveto(new_pos[0], new_pos[1]);
          RPGJS.Player.moveRoute([message.data.direction, "speed_3"]);
        }
        for (i in channels) {
          if (channels[i] === 'game-comment') {
            this.news = this.dataMapper.mapData(this.news, message.data);
          }
        }
      });
    });
    $scope.commentCreate = function($event) {
      $event.preventDefault();
      swampdragon.callRouter('send_command', 'game', {
        comment: $scope.commentForm.text,
        command: $scope.commentForm.command,
        player: $scope.playerName
      }, function(context, data) {
        return console.log(context, data);
      }, function(context, data) {
        return console.log(context, data);
      });
      $scope.commentForm.text = "";
      return $scope.commentForm.command = null;
    };
  });

}).call(this);
