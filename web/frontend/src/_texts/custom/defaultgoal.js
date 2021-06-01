const textProps = {
  name: "Title of the Goal",
  description: "Description of the Goal",
  contract: {
      assumptions: [],
      guarantees: []
  }
};
export default textProps;


/*
{
	"name": "night_patrol_34",
	"description": "During context night => start from r3, patrol r3, r4 in strict order, Strict Ordered Patrolling Location 	r3, r4",
	"context": ["night"],
	"contract": {
		"assumptions": [{
			"type": "LTL",
			"ltl_value": "true"
		}],
		"guarantees": [{
			"type": "pattern",
			"content": {
				"name": "StrictOrderPatrolling",
				"arguments": [{
					"name": "locations",
					"format": "list",
					"type": "location",
					"value": ["r3", "r4"]
				}]
			}
		}]
	}
}*/