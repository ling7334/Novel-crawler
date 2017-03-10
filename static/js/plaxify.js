// 鼠标移动视差效果
// https://github.com/404
/*
 * @example
 *  var layers = $('.js-plaxify')
 *  $.each(layers, function(index, layer){
 *    $(layer).plaxify({
 *      xRange: $(layer).data('xrange') || 0, // 水平移动范围
 *      yRange: $(layer).data('yrange') || 0, // 竖直移动范围
 *      invert: $(layer).data('invert') || false // 是否反向
 *      background: false // 是否使用背景定位实现位移
 *    })
 *  })
 *
 *  $.plax.enable({activityTarget: $('xxx')}); // 开启视差效果，activityTarget：视差容器
 */
(function($){
    var frames = 25;
    var span = 1 / frames * 1e3;
    var now = (new Date).getTime();
    var items = [];
    var container = $(window);
    var markX = null;
    var markY = null;

    function parallax(event) {

        if ((new Date).getTime() < now + span) return;
        now = (new Date).getTime();

        var offsetX = container.offset() != null ? container.offset().left : 0;
        var offsetY = container.offset() != null ? container.offset().top : 0;
        var pointX = event.pageX - offsetX;
        var pointY = event.pageY - offsetY;

        if (pointX < 0 || pointX > container.width() || pointY < 0 || pointY > container.height()){
            return;
        }

        var scaleX = pointX / container.width();
        var scaleY = pointY / container.height();
        var temp;
        var newX;
        var newY;

        for (var i = items.length; i--; ) {
            temp = items[i];
            newX = temp.startX + temp.inversionFactor * temp.xRange * scaleX;
            newY = temp.startY + temp.inversionFactor * temp.yRange * scaleY;

            if (temp.background) {
                temp.obj.css("background-position", newX + "px " + newY + "px")
            } else {
                temp.obj.css("left", newX).css("top", newY)
            }
        }
    }

    $.fn.plaxify = function(options) {
        return this.each(function() {
            var itemsLen = -1;
            var opts = {
                xRange: $(this).data("xrange") || 0,
                yRange: $(this).data("yrange") || 0,
                invert: $(this).data("invert") || false,
                background: $(this).data("background") || false
            };

            for (var i = 0; i < items.length; i++) {
                if (this === items[i].obj.get(0)) {
                    itemsLen = i;
                }
            }
            for (var n in options) {
                if (opts[n] == 0) {
                    opts[n] = options[n];
                }
            }
            opts.inversionFactor = opts.invert ? -1 : 1;
            opts.obj = $(this);

            if (opts.background) {
                pos = (opts.obj.css("background-position") || "0px 0px").split(/ /);

                if (pos.length != 2) {
                    return
                }

                x = pos[0].match(/^((-?\d+)\s*px|0+\s*%|left)$/);
                y = pos[1].match(/^((-?\d+)\s*px|0+\s*%|top)$/);

                if (!x || !y) {
                    return
                }

                opts.startX = x[2] || 0;
                opts.startY = y[2] || 0
            } else {
                var p = opts.obj.position();
                opts.obj.css({top: p.top, left: p.left, right: "", bottom: ""});
                opts.startX = this.offsetLeft;
                opts.startY = this.offsetTop
            }

            opts.startX -= opts.inversionFactor * Math.floor(opts.xRange / 2);
            opts.startY -= opts.inversionFactor * Math.floor(opts.yRange / 2);

            if (itemsLen >= 0) {
                items.splice(itemsLen, 1, opts);
            } else {
                items.push(opts);
            }
        })
    };

    // 启动/关闭视差效果
    $.plax = {
        enable: function(opts) {
            $(document).bind("mousemove.plax", function(e) {
                if (opts) {
                    container = opts.activityTarget || $(window);
                }
                parallax(e);
            });
        },
        disable: function(opts) {
            $(document).unbind("mousemove.plax");

            window.ondeviceorientation = undefined;

            if (opts && typeof opts.clearLayers === "boolean" && opts.clearLayers){
                items = [];
            }
        }
    };
})(jQuery);