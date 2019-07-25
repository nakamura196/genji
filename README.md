# genji

- [源氏物語大成 p.333 を検索する](https://nakamura196.github.io/genji/snorql/?query=SELECT+DISTINCT+%3Fmanifest+%3Fcanvas_id+WHERE+%7B%0D%0A++%3Ftaisei_page+rdfs%3Alabel+%22333%22%5E%5Exsd%3Aint+.+%0D%0A++%3Fcanvas_id+dcterms%3Asubject+%3Ftaisei_page+.+%0D%0A++%3Fcanvas_id+dcterms%3AisPartOf+%3Fmanifest+.+%0D%0A%7D)
  - [結果をMiradorで表示](http://da.dl.itc.u-tokyo.ac.jp/mirador/?manifest=https://nakamura196.github.io/genji/ugm/kyushu/manifest/10.json&canvas=https://catalog.lib.kyushu-u.ac.jp/image/411205/canvas/p3)

- [桐壺を検索する](https://nakamura196.github.io/genji/snorql/?query=SELECT+DISTINCT+%3Fmanifest+%3Fattr+WHERE+%7B%0D%0A++%3Fwork+rdfs%3Alabel+%3Flabel+.+%0D%0A++filter+regex%28%3Flabel%2C+%22%E6%A1%90%E5%A3%BA%22%29+.+%0D%0A++%3Fmanifest+dcterms%3Asubject+%3Fwork+.+%0D%0A++%3Fmanifest+dcterms%3AisPartOf+%3Fcollection+.+%0D%0A++%3Fcollection+rdfs%3Alabel+%3Fattr+.+%0D%0A%7D)
  - [結果をMiradorで表示](http://da.dl.itc.u-tokyo.ac.jp/mirador/?manifest=https://nakamura196.github.io/genji/ugm/kyushu/manifest/01.json;https://nakamura196.github.io/genji/ugm/utokyo/manifest/01.json)
