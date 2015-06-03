define([
    'freeipa/phases',
    'freeipa/reg',
    'freeipa/rpc',
    'freeipa/ipa',
    'freeipa/user'],
    function(phases, reg, rpc, IPA, user_mod) {

function get_item_by_attrval(array, attr, value) {
    for (var i=0, l=array.length; i<l; i++) {
        if (array[i][attr] === value) return array[i];
    }
    return null;
}

var exp = IPA.eduperson = {};

exp.add_eduperson_pre_op = function() {
    var facet = get_item_by_attrval(user_mod.entity_spec.facets, '$type', 'details');
    var section = get_item_by_attrval(facet.sections, 'name', 'identity');
    section.fields.push({
        name: 'edupersonaffiliation',
        $type: 'multivalued',
        label: 'Affiliation'
    });
    section.fields.push({
        name: 'edupersonnickname',
        $type: 'multivalued',
        label: 'Nickname'
    });
    section.fields.push({
        name: 'edupersonorgdn',
        $type: 'singlevalued',
        label: 'Organization DN'
    });
    section.fields.push({
        name: 'edupersonorgunitdn',
        $type: 'singlevalued',
        label: 'Organizational Unit DN'
    });
    section.fields.push({
        name: 'edupersonprimaryaffiliation',
        $type: 'singlevalued',
        label: 'Primary Affiliation'
    });
    section.fields.push({
        name: 'edupersonprincipalname',
        $type: 'singlevalued',
        label: 'Principal Name'
    });
    section.fields.push({
        name: 'edupersonprimaryorgunit',
        $type: 'singlevalued',
        label: 'Primary Organizational Unit'
    });
    section.fields.push({
        name: 'edupersontargetedid',
        $type: 'multivalued',
        label: 'Targeted ID'
    });
    section.fields.push({
        name: 'edupersonassurance',
        $type: 'multivalued',
        label: 'Assurance'
    });
    return true;
}

exp.add_eduperson_actions = function() {
    reg.action.register('user_addeduperson', exp.user_addeduperson);

    var facet = get_item_by_attrval(user_mod.entity_spec.facets, '$type', 'details');
    var section = get_item_by_attrval(facet.sections, 'name', 'identity');
    console.debug(facet.sections);

    facet.actions.push({
        $factory: IPA.object_action,
        name: 'user_addeduperson',
        method: 'addeduperson',
        label: '@i18n:actions.user_addeduperson',
        needs_confirm: false
    });
    facet.header_actions.push('user_addeduperson');

    facet.actions.push({
        $factory: IPA.object_action,
        name: 'user_deleduperson',
        method: 'deleduperson',
        label: '@i18n:actions.user_deleduperson',
        needs_confirm: true
    });
    facet.header_actions.push('user_deleduperson');

    return true;
};

phases.on('registration', exp.add_eduperson_actions);
phases.on('customization', exp.add_eduperson_pre_op);

return exp;
}); 

