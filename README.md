# lulz-scraping

## Example

Let's take the following `HTML example`:

```html
<table width="100%" id="listeEntreprise" border="0" class="zone" style="width:100%;margin-top:0px;margin-bottom:10px">
    <thead>
        <tr style="background:#7fb33e; color:#FFFFFF; font-style:'Helvetica' font-size:12px" valign="middle">
            
            <th style="margin-left:0px; width:10px; margin-right:-10px">Date</th>
            <th style="margin-left:0px, width:20%">N° RCCM</th>
            <th style="margin-left:0px, width:60%">Raison Sociale</th>
            <th style="margin-left:0px, width:20%">Statut Juridique</th>	
        </tr>
    </thead>
    <tbody>
        <tr style="font-size:12px;" id="contenu">
            <td style="padding:-1px-1px-1px-1px; margin-left:5px; width:10px; margin-right:5px; margin-right:-10px">
                08/05/2019
            </td>
            <td style="width:250px; height:10px">CI-ABJ-2019-B-10428</td>
            <td style="text-align:left; width:500px">
                <a href="https://www.cepici.ci/rapports_generes/pdf/65684.pdf" target="_blank">
                    AMADEUS ABIDJANAIS
                </a>
            </td>
            <td style="width:200px; height:10px; margin-left:0px">SARL U</td>
        </tr>
    </tbody>
</table>
```

You just have to describe your `parser.yml`:

```yml
site:
  - cepici
cepici:
  url: https://cepici.ci/views/annonces_legales/Affichage_ajax/SearchRS.php?countInit=0
  request_type: GET
  parameters:
    - search_rs
  parser:
    name: tr#contenu a
    legal_form: tr#contenu > td:nth-child(4)
    rccm_number: tr#contenu > td:nth-child(2)
    date_of_creation: tr#contenu > td:nth-child(1)
```
Output response you will get with that `parser`

```json
[
    {
        "name": "AMADEUS ABIDJANAIS",
        "legal_form": "SARL U",
        "rccm_number": "CI-ABJ-2019-B-10428",
        "date_of_creation": "08/05/2019"
    }
]
```
