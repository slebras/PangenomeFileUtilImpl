
package us.kbase.pangenomefileutil;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: PangenomeTsvFiles</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "genomes_path",
    "orthologs_path",
    "shock_id"
})
public class PangenomeTsvFiles {

    @JsonProperty("genomes_path")
    private String genomesPath;
    @JsonProperty("orthologs_path")
    private String orthologsPath;
    @JsonProperty("shock_id")
    private String shockId;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("genomes_path")
    public String getGenomesPath() {
        return genomesPath;
    }

    @JsonProperty("genomes_path")
    public void setGenomesPath(String genomesPath) {
        this.genomesPath = genomesPath;
    }

    public PangenomeTsvFiles withGenomesPath(String genomesPath) {
        this.genomesPath = genomesPath;
        return this;
    }

    @JsonProperty("orthologs_path")
    public String getOrthologsPath() {
        return orthologsPath;
    }

    @JsonProperty("orthologs_path")
    public void setOrthologsPath(String orthologsPath) {
        this.orthologsPath = orthologsPath;
    }

    public PangenomeTsvFiles withOrthologsPath(String orthologsPath) {
        this.orthologsPath = orthologsPath;
        return this;
    }

    @JsonProperty("shock_id")
    public String getShockId() {
        return shockId;
    }

    @JsonProperty("shock_id")
    public void setShockId(String shockId) {
        this.shockId = shockId;
    }

    public PangenomeTsvFiles withShockId(String shockId) {
        this.shockId = shockId;
        return this;
    }

    @JsonAnyGetter
    public Map<String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public String toString() {
        return ((((((((("PangenomeTsvFiles"+" [genomesPath=")+ genomesPath)+", orthologsPath=")+ orthologsPath)+", shockId=")+ shockId)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
