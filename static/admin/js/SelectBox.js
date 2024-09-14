<<<<<<< Updated upstream
(function($) {
    'use strict';
    var SelectBox = {
        cache: {},
        init: function(id) {
            var box = document.getElementById(id);
            var node;
            SelectBox.cache[id] = [];
            var cache = SelectBox.cache[id];
            var boxOptions = box.options;
            var boxOptionsLength = boxOptions.length;
            for (var i = 0, j = boxOptionsLength; i < j; i++) {
                node = boxOptions[i];
=======
'use strict';
{
    const SelectBox = {
        cache: {},
        init: function(id) {
            const box = document.getElementById(id);
            SelectBox.cache[id] = [];
            const cache = SelectBox.cache[id];
            for (const node of box.options) {
>>>>>>> Stashed changes
                cache.push({value: node.value, text: node.text, displayed: 1});
            }
        },
        redisplay: function(id) {
            // Repopulate HTML select box from cache
<<<<<<< Updated upstream
            var box = document.getElementById(id);
            var node;
            $(box).empty(); // clear all options
            var new_options = box.outerHTML.slice(0, -9); // grab just the opening tag
            var cache = SelectBox.cache[id];
            for (var i = 0, j = cache.length; i < j; i++) {
                node = cache[i];
                if (node.displayed) {
                    var new_option = new Option(node.text, node.value, false, false);
                    // Shows a tooltip when hovering over the option
                    new_option.setAttribute("title", node.text);
                    new_options += new_option.outerHTML;
                }
            }
            new_options += '</select>';
            box.outerHTML = new_options;
=======
            const box = document.getElementById(id);
            const scroll_value_from_top = box.scrollTop;
            box.innerHTML = '';
            for (const node of SelectBox.cache[id]) {
                if (node.displayed) {
                    const new_option = new Option(node.text, node.value, false, false);
                    // Shows a tooltip when hovering over the option
                    new_option.title = node.text;
                    box.appendChild(new_option);
                }
            }
            box.scrollTop = scroll_value_from_top;
>>>>>>> Stashed changes
        },
        filter: function(id, text) {
            // Redisplay the HTML select box, displaying only the choices containing ALL
            // the words in text. (It's an AND search.)
<<<<<<< Updated upstream
            var tokens = text.toLowerCase().split(/\s+/);
            var node, token;
            var cache = SelectBox.cache[id];
            for (var i = 0, j = cache.length; i < j; i++) {
                node = cache[i];
                node.displayed = 1;
                var node_text = node.text.toLowerCase();
                var numTokens = tokens.length;
                for (var k = 0; k < numTokens; k++) {
                    token = tokens[k];
                    if (node_text.indexOf(token) === -1) {
=======
            const tokens = text.toLowerCase().split(/\s+/);
            for (const node of SelectBox.cache[id]) {
                node.displayed = 1;
                const node_text = node.text.toLowerCase();
                for (const token of tokens) {
                    if (!node_text.includes(token)) {
>>>>>>> Stashed changes
                        node.displayed = 0;
                        break; // Once the first token isn't found we're done
                    }
                }
            }
            SelectBox.redisplay(id);
        },
<<<<<<< Updated upstream
        delete_from_cache: function(id, value) {
            var node, delete_index = null;
            var cache = SelectBox.cache[id];
            for (var i = 0, j = cache.length; i < j; i++) {
                node = cache[i];
=======
        get_hidden_node_count(id) {
            const cache = SelectBox.cache[id] || [];
            return cache.filter(node => node.displayed === 0).length;
        },
        delete_from_cache: function(id, value) {
            let delete_index = null;
            const cache = SelectBox.cache[id];
            for (const [i, node] of cache.entries()) {
>>>>>>> Stashed changes
                if (node.value === value) {
                    delete_index = i;
                    break;
                }
            }
            cache.splice(delete_index, 1);
        },
        add_to_cache: function(id, option) {
            SelectBox.cache[id].push({value: option.value, text: option.text, displayed: 1});
        },
        cache_contains: function(id, value) {
            // Check if an item is contained in the cache
<<<<<<< Updated upstream
            var node;
            var cache = SelectBox.cache[id];
            for (var i = 0, j = cache.length; i < j; i++) {
                node = cache[i];
=======
            for (const node of SelectBox.cache[id]) {
>>>>>>> Stashed changes
                if (node.value === value) {
                    return true;
                }
            }
            return false;
        },
        move: function(from, to) {
<<<<<<< Updated upstream
            var from_box = document.getElementById(from);
            var option;
            var boxOptions = from_box.options;
            var boxOptionsLength = boxOptions.length;
            for (var i = 0, j = boxOptionsLength; i < j; i++) {
                option = boxOptions[i];
                var option_value = option.value;
=======
            const from_box = document.getElementById(from);
            for (const option of from_box.options) {
                const option_value = option.value;
>>>>>>> Stashed changes
                if (option.selected && SelectBox.cache_contains(from, option_value)) {
                    SelectBox.add_to_cache(to, {value: option_value, text: option.text, displayed: 1});
                    SelectBox.delete_from_cache(from, option_value);
                }
            }
            SelectBox.redisplay(from);
            SelectBox.redisplay(to);
        },
        move_all: function(from, to) {
<<<<<<< Updated upstream
            var from_box = document.getElementById(from);
            var option;
            var boxOptions = from_box.options;
            var boxOptionsLength = boxOptions.length;
            for (var i = 0, j = boxOptionsLength; i < j; i++) {
                option = boxOptions[i];
                var option_value = option.value;
=======
            const from_box = document.getElementById(from);
            for (const option of from_box.options) {
                const option_value = option.value;
>>>>>>> Stashed changes
                if (SelectBox.cache_contains(from, option_value)) {
                    SelectBox.add_to_cache(to, {value: option_value, text: option.text, displayed: 1});
                    SelectBox.delete_from_cache(from, option_value);
                }
            }
            SelectBox.redisplay(from);
            SelectBox.redisplay(to);
        },
        sort: function(id) {
            SelectBox.cache[id].sort(function(a, b) {
                a = a.text.toLowerCase();
                b = b.text.toLowerCase();
<<<<<<< Updated upstream
                try {
                    if (a > b) {
                        return 1;
                    }
                    if (a < b) {
                        return -1;
                    }
                }
                catch (e) {
                    // silently fail on IE 'unknown' exception
=======
                if (a > b) {
                    return 1;
                }
                if (a < b) {
                    return -1;
>>>>>>> Stashed changes
                }
                return 0;
            } );
        },
        select_all: function(id) {
<<<<<<< Updated upstream
            var box = document.getElementById(id);
            var boxOptions = box.options;
            var boxOptionsLength = boxOptions.length;
            for (var i = 0; i < boxOptionsLength; i++) {
                boxOptions[i].selected = 'selected';
=======
            const box = document.getElementById(id);
            for (const option of box.options) {
                option.selected = true;
>>>>>>> Stashed changes
            }
        }
    };
    window.SelectBox = SelectBox;
<<<<<<< Updated upstream
})(django.jQuery);
=======
}
>>>>>>> Stashed changes
