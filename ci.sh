#!/bin/sh
# CI gate: nothing ships unexecuted.
# Runs the verification suite and all three drivers; fails on any [FAIL]
# or crash. ~30 min (trace_rates dominates). (Every v2-audit defect -- a NameError, a driver on
# the wrong system, an off-by-one in sampling -- would have been caught
# by one execution of this script.)
fail=0
python3 verify_all.py | tee /tmp/ci_verify.log || fail=1
if grep -q "\[FAIL\]" /tmp/ci_verify.log; then echo "CI: verify_all has FAILs"; fail=1; fi
for d in run_qg.py run_plan2.py run_atlas.py prism_L.py gadgets.py trace_rates.py; do
  echo "== $d =="
  python3 "$d" || { echo "CI: $d crashed"; fail=1; }
done
echo "== campaign.py --quick =="
rm -f campaign_quick.csv
python3 campaign.py --quick || { echo "CI: campaign.py crashed"; fail=1; }
[ "$fail" -eq 0 ] && echo "CI: all green" || echo "CI: FAILED"
exit $fail
