#!/usr/bin/env bash
BASE="${1:-https://calculateallinone.vercel.app}"
fail=0

while read -r path
do
  if [ -z "$path" ]
  then
    continue
  fi
  result=$(curl -s -o /tmp/page.html -L --max-redirs 3 -w "%{http_code} %{num_redirects} %{url_effective}" "${BASE}${path}")
  code=$(echo "$result" | cut -d " " -f 1)
  hops=$(echo "$result" | cut -d " " -f 2)
  echo "$result $path"
  if [ "$code" != "200" ]
  then
    echo "STATUS FAIL $path"
    fail=1
  fi
  if [ "$hops" != "0" ]
  then
    echo "REDIRECT FAIL $path"
    fail=1
  fi
  canon=$(grep -o 'rel="canonical" href="[^"]*"' /tmp/page.html | head -n 1)
  expected="rel=\"canonical\" href=\"${BASE}${path}\""
  if [ "$canon" != "$expected" ]
  then
    echo "CANONICAL FAIL $path: $canon"
    fail=1
  fi
done < urls.txt

while read -r path
do
  if [ -z "$path" ]
  then
    continue
  fi
  line=$(curl -s -o /dev/null -w "%{http_code} %{redirect_url}" "${BASE}${path}")
  echo "$line $path"
  expected_redirect="${BASE}${path}/"
  if [ "$line" != "301 ${expected_redirect}" ] && [ "$line" != "308 ${expected_redirect}" ]
  then
    echo "NO-SLASH REDIRECT FAIL $path"
    fail=1
  fi
done < no-slash.txt

curl -s "${BASE}/sitemap.xml" > /tmp/sitemap.xml
if [ ! -s /tmp/sitemap.xml ]
then
  echo "SITEMAP EMPTY"
  fail=1
fi

while read -r path
do
  if [ -z "$path" ]
  then
    continue
  fi
  if ! grep -Fq "${BASE}${path}" /tmp/sitemap.xml
  then
    echo "MISSING FROM SITEMAP $path"
    fail=1
  fi
done < indexable.txt

while read -r path
do
  if [ -z "$path" ]
  then
    continue
  fi
  if grep -Fq "${BASE}${path}" /tmp/sitemap.xml
  then
    echo "NOINDEX PAGE IN SITEMAP $path"
    fail=1
  fi
  if ! curl -s "${BASE}${path}" | grep -q 'name="robots" content="noindex'
  then
    echo "NOINDEX TAG MISSING $path"
    fail=1
  fi
done < noindex.txt

while read -r path
do
  if [ -z "$path" ]
  then
    continue
  fi
  curl -s "${BASE}${path}" | grep -o "<title>[^<]*</title>"
done < indexable.txt | sort | uniq -d > /tmp/dup_titles.txt
if [ -s /tmp/dup_titles.txt ]
then
  echo "DUPLICATE TITLES"
  cat /tmp/dup_titles.txt
  fail=1
fi

if [ "$fail" -eq 0 ]
then
  echo "ALL CHECKS PASSED"
fi
exit $fail
