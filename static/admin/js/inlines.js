/*global DateTimeShortcuts, SelectFilter*/
/**
 * Django admin inlines
 *
 * Based on jQuery Formset 1.1
 * @author Stanislaus Madueke (stan DOT madueke AT gmail DOT com)
 * @requires jQuery 1.2.6 or later
 *
 * Copyright (c) 2009, Stanislaus Madueke
 * All rights reserved.
 *
 * Spiced up with Code from Zain Memon's GSoC project 2009
 * and modified for Django by Jannis Leidel, Travis Swicegood and Julien Phalip.
 *
 * Licensed under the New BSD License
 * See: https://opensource.org/licenses/bsd-license.php
 */
<<<<<<< Updated upstream
(function($) {
    'use strict';
    $.fn.formset = function(opts) {
        var options = $.extend({}, $.fn.formset.defaults, opts);
        var $this = $(this);
        var $parent = $this.parent();
        var updateElementIndex = function(el, prefix, ndx) {
            var id_regex = new RegExp("(" + prefix + "-(\\d+|__prefix__))");
            var replacement = prefix + "-" + ndx;
=======
'use strict';
{
    const $ = django.jQuery;
    $.fn.formset = function(opts) {
        const options = $.extend({}, $.fn.formset.defaults, opts);
        const $this = $(this);
        const $parent = $this.parent();
        const updateElementIndex = function(el, prefix, ndx) {
            const id_regex = new RegExp("(" + prefix + "-(\\d+|__prefix__))");
            const replacement = prefix + "-" + ndx;
>>>>>>> Stashed changes
            if ($(el).prop("for")) {
                $(el).prop("for", $(el).prop("for").replace(id_regex, replacement));
            }
            if (el.id) {
                el.id = el.id.replace(id_regex, replacement);
            }
            if (el.name) {
                el.name = el.name.replace(id_regex, replacement);
            }
        };
<<<<<<< Updated upstream
        var totalForms = $("#id_" + options.prefix + "-TOTAL_FORMS").prop("autocomplete", "off");
        var nextIndex = parseInt(totalForms.val(), 10);
        var maxForms = $("#id_" + options.prefix + "-MAX_NUM_FORMS").prop("autocomplete", "off");
        // only show the add button if we are allowed to add more items,
        // note that max_num = None translates to a blank string.
        var showAddButton = maxForms.val() === '' || (maxForms.val() - totalForms.val()) > 0;
        $this.each(function(i) {
            $(this).not("." + options.emptyCssClass).addClass(options.formCssClass);
        });
        if ($this.length && showAddButton) {
            var addButton = options.addButton;
=======
        const totalForms = $("#id_" + options.prefix + "-TOTAL_FORMS").prop("autocomplete", "off");
        let nextIndex = parseInt(totalForms.val(), 10);
        const maxForms = $("#id_" + options.prefix + "-MAX_NUM_FORMS").prop("autocomplete", "off");
        const minForms = $("#id_" + options.prefix + "-MIN_NUM_FORMS").prop("autocomplete", "off");
        let addButton;

        /**
         * The "Add another MyModel" button below the inline forms.
         */
        const addInlineAddButton = function() {
>>>>>>> Stashed changes
            if (addButton === null) {
                if ($this.prop("tagName") === "TR") {
                    // If forms are laid out as table rows, insert the
                    // "add" button in a new table row:
<<<<<<< Updated upstream
                    var numCols = this.eq(-1).children().length;
=======
                    const numCols = $this.eq(-1).children().length;
>>>>>>> Stashed changes
                    $parent.append('<tr class="' + options.addCssClass + '"><td colspan="' + numCols + '"><a href="#">' + options.addText + "</a></tr>");
                    addButton = $parent.find("tr:last a");
                } else {
                    // Otherwise, insert it immediately after the last form:
                    $this.filter(":last").after('<div class="' + options.addCssClass + '"><a href="#">' + options.addText + "</a></div>");
                    addButton = $this.filter(":last").next().find("a");
                }
            }
<<<<<<< Updated upstream
            addButton.on('click', function(e) {
                e.preventDefault();
                var template = $("#" + options.prefix + "-empty");
                var row = template.clone(true);
                row.removeClass(options.emptyCssClass)
                    .addClass(options.formCssClass)
                    .attr("id", options.prefix + "-" + nextIndex);
                if (row.is("tr")) {
                    // If the forms are laid out in table rows, insert
                    // the remove button into the last table cell:
                    row.children(":last").append('<div><a class="' + options.deleteCssClass + '" href="#">' + options.deleteText + "</a></div>");
                } else if (row.is("ul") || row.is("ol")) {
                    // If they're laid out as an ordered/unordered list,
                    // insert an <li> after the last list item:
                    row.append('<li><a class="' + options.deleteCssClass + '" href="#">' + options.deleteText + "</a></li>");
                } else {
                    // Otherwise, just insert the remove button as the
                    // last child element of the form's container:
                    row.children(":first").append('<span><a class="' + options.deleteCssClass + '" href="#">' + options.deleteText + "</a></span>");
                }
                row.find("*").each(function() {
                    updateElementIndex(this, options.prefix, totalForms.val());
                });
                // Insert the new form when it has been fully edited
                row.insertBefore($(template));
                // Update number of total forms
                $(totalForms).val(parseInt(totalForms.val(), 10) + 1);
                nextIndex += 1;
                // Hide add button in case we've hit the max, except we want to add infinitely
                if ((maxForms.val() !== '') && (maxForms.val() - totalForms.val()) <= 0) {
                    addButton.parent().hide();
                }
                // The delete button of each row triggers a bunch of other things
                row.find("a." + options.deleteCssClass).on('click', function(e1) {
                    e1.preventDefault();
                    // Remove the parent form containing this button:
                    row.remove();
                    nextIndex -= 1;
                    // If a post-delete callback was provided, call it with the deleted form:
                    if (options.removed) {
                        options.removed(row);
                    }
                    $(document).trigger('formset:removed', [row, options.prefix]);
                    // Update the TOTAL_FORMS form count.
                    var forms = $("." + options.formCssClass);
                    $("#id_" + options.prefix + "-TOTAL_FORMS").val(forms.length);
                    // Show add button again once we drop below max
                    if ((maxForms.val() === '') || (maxForms.val() - forms.length) > 0) {
                        addButton.parent().show();
                    }
                    // Also, update names and ids for all remaining form controls
                    // so they remain in sequence:
                    var i, formCount;
                    var updateElementCallback = function() {
                        updateElementIndex(this, options.prefix, i);
                    };
                    for (i = 0, formCount = forms.length; i < formCount; i++) {
                        updateElementIndex($(forms).get(i), options.prefix, i);
                        $(forms.get(i)).find("*").each(updateElementCallback);
                    }
                });
                // If a post-add callback was supplied, call it with the added form:
                if (options.added) {
                    options.added(row);
                }
                $(document).trigger('formset:added', [row, options.prefix]);
            });
        }
=======
            addButton.on('click', addInlineClickHandler);
        };

        const addInlineClickHandler = function(e) {
            e.preventDefault();
            const template = $("#" + options.prefix + "-empty");
            const row = template.clone(true);
            row.removeClass(options.emptyCssClass)
                .addClass(options.formCssClass)
                .attr("id", options.prefix + "-" + nextIndex);
            addInlineDeleteButton(row);
            row.find("*").each(function() {
                updateElementIndex(this, options.prefix, totalForms.val());
            });
            // Insert the new form when it has been fully edited.
            row.insertBefore($(template));
            // Update number of total forms.
            $(totalForms).val(parseInt(totalForms.val(), 10) + 1);
            nextIndex += 1;
            // Hide the add button if there's a limit and it's been reached.
            if ((maxForms.val() !== '') && (maxForms.val() - totalForms.val()) <= 0) {
                addButton.parent().hide();
            }
            // Show the remove buttons if there are more than min_num.
            toggleDeleteButtonVisibility(row.closest('.inline-group'));

            // Pass the new form to the post-add callback, if provided.
            if (options.added) {
                options.added(row);
            }
            row.get(0).dispatchEvent(new CustomEvent("formset:added", {
                bubbles: true,
                detail: {
                    formsetName: options.prefix
                }
            }));
        };

        /**
         * The "X" button that is part of every unsaved inline.
         * (When saved, it is replaced with a "Delete" checkbox.)
         */
        const addInlineDeleteButton = function(row) {
            if (row.is("tr")) {
                // If the forms are laid out in table rows, insert
                // the remove button into the last table cell:
                row.children(":last").append('<div><a class="' + options.deleteCssClass + '" href="#">' + options.deleteText + "</a></div>");
            } else if (row.is("ul") || row.is("ol")) {
                // If they're laid out as an ordered/unordered list,
                // insert an <li> after the last list item:
                row.append('<li><a class="' + options.deleteCssClass + '" href="#">' + options.deleteText + "</a></li>");
            } else {
                // Otherwise, just insert the remove button as the
                // last child element of the form's container:
                row.children(":first").append('<span><a class="' + options.deleteCssClass + '" href="#">' + options.deleteText + "</a></span>");
            }
            // Add delete handler for each row.
            row.find("a." + options.deleteCssClass).on('click', inlineDeleteHandler.bind(this));
        };

        const inlineDeleteHandler = function(e1) {
            e1.preventDefault();
            const deleteButton = $(e1.target);
            const row = deleteButton.closest('.' + options.formCssClass);
            const inlineGroup = row.closest('.inline-group');
            // Remove the parent form containing this button,
            // and also remove the relevant row with non-field errors:
            const prevRow = row.prev();
            if (prevRow.length && prevRow.hasClass('row-form-errors')) {
                prevRow.remove();
            }
            row.remove();
            nextIndex -= 1;
            // Pass the deleted form to the post-delete callback, if provided.
            if (options.removed) {
                options.removed(row);
            }
            document.dispatchEvent(new CustomEvent("formset:removed", {
                detail: {
                    formsetName: options.prefix
                }
            }));
            // Update the TOTAL_FORMS form count.
            const forms = $("." + options.formCssClass);
            $("#id_" + options.prefix + "-TOTAL_FORMS").val(forms.length);
            // Show add button again once below maximum number.
            if ((maxForms.val() === '') || (maxForms.val() - forms.length) > 0) {
                addButton.parent().show();
            }
            // Hide the remove buttons if at min_num.
            toggleDeleteButtonVisibility(inlineGroup);
            // Also, update names and ids for all remaining form controls so
            // they remain in sequence:
            let i, formCount;
            const updateElementCallback = function() {
                updateElementIndex(this, options.prefix, i);
            };
            for (i = 0, formCount = forms.length; i < formCount; i++) {
                updateElementIndex($(forms).get(i), options.prefix, i);
                $(forms.get(i)).find("*").each(updateElementCallback);
            }
        };

        const toggleDeleteButtonVisibility = function(inlineGroup) {
            if ((minForms.val() !== '') && (minForms.val() - totalForms.val()) >= 0) {
                inlineGroup.find('.inline-deletelink').hide();
            } else {
                inlineGroup.find('.inline-deletelink').show();
            }
        };

        $this.each(function(i) {
            $(this).not("." + options.emptyCssClass).addClass(options.formCssClass);
        });

        // Create the delete buttons for all unsaved inlines:
        $this.filter('.' + options.formCssClass + ':not(.has_original):not(.' + options.emptyCssClass + ')').each(function() {
            addInlineDeleteButton($(this));
        });
        toggleDeleteButtonVisibility($this);

        // Create the add button, initially hidden.
        addButton = options.addButton;
        addInlineAddButton();

        // Show the add button if allowed to add more items.
        // Note that max_num = None translates to a blank string.
        const showAddButton = maxForms.val() === '' || (maxForms.val() - totalForms.val()) > 0;
        if ($this.length && showAddButton) {
            addButton.parent().show();
        } else {
            addButton.parent().hide();
        }

>>>>>>> Stashed changes
        return this;
    };

    /* Setup plugin defaults */
    $.fn.formset.defaults = {
        prefix: "form", // The form prefix for your django formset
        addText: "add another", // Text for the add link
        deleteText: "remove", // Text for the delete link
        addCssClass: "add-row", // CSS class applied to the add link
        deleteCssClass: "delete-row", // CSS class applied to the delete link
        emptyCssClass: "empty-row", // CSS class applied to the empty row
        formCssClass: "dynamic-form", // CSS class applied to each form in a formset
        added: null, // Function called each time a new form is added
        removed: null, // Function called each time a form is deleted
        addButton: null // Existing add button to use
    };


    // Tabular inlines ---------------------------------------------------------
    $.fn.tabularFormset = function(selector, options) {
<<<<<<< Updated upstream
        var $rows = $(this);
        var alternatingRows = function(row) {
            $(selector).not(".add-row").removeClass("row1 row2")
                .filter(":even").addClass("row1").end()
                .filter(":odd").addClass("row2");
        };

        var reinitDateTimeShortCuts = function() {
=======
        const $rows = $(this);

        const reinitDateTimeShortCuts = function() {
>>>>>>> Stashed changes
            // Reinitialize the calendar and clock widgets by force
            if (typeof DateTimeShortcuts !== "undefined") {
                $(".datetimeshortcuts").remove();
                DateTimeShortcuts.init();
            }
        };

<<<<<<< Updated upstream
        var updateSelectFilter = function() {
=======
        const updateSelectFilter = function() {
>>>>>>> Stashed changes
            // If any SelectFilter widgets are a part of the new form,
            // instantiate a new SelectFilter instance for it.
            if (typeof SelectFilter !== 'undefined') {
                $('.selectfilter').each(function(index, value) {
<<<<<<< Updated upstream
                    var namearr = value.name.split('-');
                    SelectFilter.init(value.id, namearr[namearr.length - 1], false);
                });
                $('.selectfilterstacked').each(function(index, value) {
                    var namearr = value.name.split('-');
                    SelectFilter.init(value.id, namearr[namearr.length - 1], true);
=======
                    SelectFilter.init(value.id, this.dataset.fieldName, false);
                });
                $('.selectfilterstacked').each(function(index, value) {
                    SelectFilter.init(value.id, this.dataset.fieldName, true);
>>>>>>> Stashed changes
                });
            }
        };

<<<<<<< Updated upstream
        var initPrepopulatedFields = function(row) {
            row.find('.prepopulated_field').each(function() {
                var field = $(this),
=======
        const initPrepopulatedFields = function(row) {
            row.find('.prepopulated_field').each(function() {
                const field = $(this),
>>>>>>> Stashed changes
                    input = field.find('input, select, textarea'),
                    dependency_list = input.data('dependency_list') || [],
                    dependencies = [];
                $.each(dependency_list, function(i, field_name) {
                    dependencies.push('#' + row.find('.field-' + field_name).find('input, select, textarea').attr('id'));
                });
                if (dependencies.length) {
                    input.prepopulate(dependencies, input.attr('maxlength'));
                }
            });
        };

        $rows.formset({
            prefix: options.prefix,
            addText: options.addText,
            formCssClass: "dynamic-" + options.prefix,
            deleteCssClass: "inline-deletelink",
            deleteText: options.deleteText,
            emptyCssClass: "empty-form",
<<<<<<< Updated upstream
            removed: alternatingRows,
=======
>>>>>>> Stashed changes
            added: function(row) {
                initPrepopulatedFields(row);
                reinitDateTimeShortCuts();
                updateSelectFilter();
<<<<<<< Updated upstream
                alternatingRows(row);
=======
>>>>>>> Stashed changes
            },
            addButton: options.addButton
        });

        return $rows;
    };

    // Stacked inlines ---------------------------------------------------------
    $.fn.stackedFormset = function(selector, options) {
<<<<<<< Updated upstream
        var $rows = $(this);
        var updateInlineLabel = function(row) {
            $(selector).find(".inline_label").each(function(i) {
                var count = i + 1;
=======
        const $rows = $(this);
        const updateInlineLabel = function(row) {
            $(selector).find(".inline_label").each(function(i) {
                const count = i + 1;
>>>>>>> Stashed changes
                $(this).html($(this).html().replace(/(#\d+)/g, "#" + count));
            });
        };

<<<<<<< Updated upstream
        var reinitDateTimeShortCuts = function() {
=======
        const reinitDateTimeShortCuts = function() {
>>>>>>> Stashed changes
            // Reinitialize the calendar and clock widgets by force, yuck.
            if (typeof DateTimeShortcuts !== "undefined") {
                $(".datetimeshortcuts").remove();
                DateTimeShortcuts.init();
            }
        };

<<<<<<< Updated upstream
        var updateSelectFilter = function() {
            // If any SelectFilter widgets were added, instantiate a new instance.
            if (typeof SelectFilter !== "undefined") {
                $(".selectfilter").each(function(index, value) {
                    var namearr = value.name.split('-');
                    SelectFilter.init(value.id, namearr[namearr.length - 1], false);
                });
                $(".selectfilterstacked").each(function(index, value) {
                    var namearr = value.name.split('-');
                    SelectFilter.init(value.id, namearr[namearr.length - 1], true);
=======
        const updateSelectFilter = function() {
            // If any SelectFilter widgets were added, instantiate a new instance.
            if (typeof SelectFilter !== "undefined") {
                $(".selectfilter").each(function(index, value) {
                    SelectFilter.init(value.id, this.dataset.fieldName, false);
                });
                $(".selectfilterstacked").each(function(index, value) {
                    SelectFilter.init(value.id, this.dataset.fieldName, true);
>>>>>>> Stashed changes
                });
            }
        };

<<<<<<< Updated upstream
        var initPrepopulatedFields = function(row) {
            row.find('.prepopulated_field').each(function() {
                var field = $(this),
=======
        const initPrepopulatedFields = function(row) {
            row.find('.prepopulated_field').each(function() {
                const field = $(this),
>>>>>>> Stashed changes
                    input = field.find('input, select, textarea'),
                    dependency_list = input.data('dependency_list') || [],
                    dependencies = [];
                $.each(dependency_list, function(i, field_name) {
<<<<<<< Updated upstream
                    dependencies.push('#' + row.find('.form-row .field-' + field_name).find('input, select, textarea').attr('id'));
=======
                    // Dependency in a fieldset.
                    let field_element = row.find('.form-row .field-' + field_name);
                    // Dependency without a fieldset.
                    if (!field_element.length) {
                        field_element = row.find('.form-row.field-' + field_name);
                    }
                    dependencies.push('#' + field_element.find('input, select, textarea').attr('id'));
>>>>>>> Stashed changes
                });
                if (dependencies.length) {
                    input.prepopulate(dependencies, input.attr('maxlength'));
                }
            });
        };

        $rows.formset({
            prefix: options.prefix,
            addText: options.addText,
            formCssClass: "dynamic-" + options.prefix,
            deleteCssClass: "inline-deletelink",
            deleteText: options.deleteText,
            emptyCssClass: "empty-form",
            removed: updateInlineLabel,
            added: function(row) {
                initPrepopulatedFields(row);
                reinitDateTimeShortCuts();
                updateSelectFilter();
                updateInlineLabel(row);
            },
            addButton: options.addButton
        });

        return $rows;
    };

    $(document).ready(function() {
        $(".js-inline-admin-formset").each(function() {
<<<<<<< Updated upstream
            var data = $(this).data(),
                inlineOptions = data.inlineFormset,
                selector;
=======
            const data = $(this).data(),
                inlineOptions = data.inlineFormset;
            let selector;
>>>>>>> Stashed changes
            switch(data.inlineType) {
            case "stacked":
                selector = inlineOptions.name + "-group .inline-related";
                $(selector).stackedFormset(selector, inlineOptions.options);
                break;
            case "tabular":
<<<<<<< Updated upstream
                selector = inlineOptions.name + "-group .tabular.inline-related tbody:first > tr";
=======
                selector = inlineOptions.name + "-group .tabular.inline-related tbody:first > tr.form-row";
>>>>>>> Stashed changes
                $(selector).tabularFormset(selector, inlineOptions.options);
                break;
            }
        });
    });
<<<<<<< Updated upstream
})(django.jQuery);
=======
}
>>>>>>> Stashed changes
