"""
  Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.

  Permission is hereby granted, free of charge, to any person obtaining a copy of this
  software and associated documentation files (the "Software"), to deal in the Software
  without restriction, including without limitation the rights to use, copy, modify,
  merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
  permit persons to whom the Software is furnished to do so.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
  PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
  HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
  OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
  SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""


import re
from cfnlint.rules import CloudFormationLintRule, RuleMatch

LINT_ERROR_MESSAGE = "Hard-coded account IDs are unacceptable."



def determine_account_id_in_principal(resource_path, resource):
    return re.search(r"[0-9]{12}", str(resource))


class IAMNoAccountNumber(CloudFormationLintRule):
    """Check for hard-coded account IDs."""

    id = "EIAMAccountIDInPrincipal"
    shortdesc = "Hard-coded account IDs are unacceptable."
    description = "Hard-coded account IDs are unacceptable."
    source_url = "https://github.com/aws-ia/cfn-ia-rules/blob/main/cfn_ia_rules/rules/security/iam_no_account_number.py"
    tags = ["iam"]
    SEARCH_PROPS = ["Principal"]
    CFN_NAG_RULES = ["W21", "W15"] 
    def match(self, cfn):
        """Basic Matching"""
        violation_matches = []
        term_matches = []
        for prop in self.SEARCH_PROPS:
            term_matches += cfn.search_deep_keys(prop)
        for tm in term_matches:
            violating_principal = determine_account_id_in_principal(tm[:-1], tm[-1])
            if violating_principal:
                violation_matches.append(RuleMatch(tm[:-1], LINT_ERROR_MESSAGE))
        return violation_matches
