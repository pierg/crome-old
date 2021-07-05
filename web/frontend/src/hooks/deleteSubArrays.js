function isSubArray(master, sub) {
    return master.join('|').includes(sub.join('|'));
};

function deleteSubArrays(table) {
    let result = []
    let valid;
    for (let i in table) {
        valid = true
        for (let j in table) {
            if (i !== j) {
                if (isSubArray(table[j], table[i])) {
                    valid = false
                }
            }
        }
        if (valid) {
            result.push(table[i]);
        }
    }
    return result;
};
